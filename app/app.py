from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
import hashlib
import sqlite3
import random
from datetime import datetime, timedelta
from contextlib import contextmanager

app = Flask(__name__)
app.secret_key = "smartbank-dev-secret-key"
DB_NAME = "smartbank.db"

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartBank Login</title>
</head>
<body>
    <h1>SmartBank Secure Login</h1>

    <form method="POST" action="/login">
        <label for="username">Username</label>
        <input id="username" name="username" type="text">

        <br><br>

        <label for="password">Password</label>
        <input id="password" name="password" type="password">

        <br><br>

        <button id="login" type="submit">Login</button>
    </form>

    {% if error %}
        <p id="error">{{ error }}</p>
    {% endif %}
</body>
</html>
"""


MFA_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>SmartBank MFA</title>
</head>
<body>
    <h1>Multi-Factor Authentication</h1>

    <p id="mfa-message">
        Valid credentials verified. Enter your MFA code.
    </p>

    <form method="POST" action="/verify-mfa">
        
        <label for="otp">MFA Code</label>
        <input id="otp" name="otp" type="text">

        <br><br>

        <button id="verify-mfa" type="submit">Verify</button>
    </form>
    
    <br><br>

    <form method="POST" action="/resend-mfa">
        <button id="resend-mfa" type="submit">Resend OTP</button>
    </form>
    
    {% if error %}
        <p id="mfa-error">{{ error }}</p>
    {% endif %}
    
    {% if message %}
        <p id="mfa-message-success">{{ message }}</p>
    {% endif %}
</body>
</html>
"""


def get_connection():
    return sqlite3.connect(DB_NAME)
@contextmanager
def get_db():
    connection = get_connection()

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_otp():
    return str(random.randint(100000, 999999))

def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            active INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            success INTEGER,
            attempt_time TEXT
        )
    """)

    valid_user_password = hash_password("ValidPassword123")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mfa_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            otp_code TEXT NOT NULL,
            created_time TEXT NOT NULL,
            expiry_time TEXT NOT NULL,
            attempts INTEGER DEFAULT 0,
            status TEXT DEFAULT 'ACTIVE'
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password_hash, active)
        VALUES (?, ?, ?)
    """, ("smartbank_user", valid_user_password, 1))
    
    inactive_user_password = hash_password("InactivePassword123")

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password_hash, active)
        VALUES (?, ?, ?)
    """, ("inactive_user", inactive_user_password, 0))

    connection.commit()
    connection.close()
    

def log_login_attempt(username, success):
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO login_audit (username, success, attempt_time)
            VALUES (?, ?, ?)
        """, (
            username,
            success,
            datetime.now().isoformat()
        ))
    
def create_mfa_session(username):
    otp = generate_otp()

    created_time = datetime.now()
    expiry_time = created_time + timedelta(minutes=5)

    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO mfa_sessions
            (username, otp_code, created_time, expiry_time, attempts, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            username,
            otp,
            created_time.isoformat(),
            expiry_time.isoformat(),
            0,
            "ACTIVE"
        ))

        mfa_session_id = cursor.lastrowid

    return mfa_session_id, otp


def verify_mfa_code(mfa_session_id, otp):
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, otp_code, expiry_time, attempts, status
            FROM mfa_sessions
            WHERE id = ?
        """, (mfa_session_id,))

        mfa_session = cursor.fetchone()
    

    if not mfa_session:
        return "NOT_FOUND"

    session_id, stored_otp, expiry_time, attempts, status = mfa_session

    # Session already locked
    if status == "LOCKED":
        return "LOCKED"

    # Session already verified
    if status == "VERIFIED":
        return "ALREADY_VERIFIED"

    # Session was replaced by a new OTP
    if status == "SUPERSEDED":
        return "SUPERSEDED"

    # Check OTP expiry
    if datetime.now() > datetime.fromisoformat(expiry_time):
        return "EXPIRED"
    
    # Check OTP
    if otp != stored_otp:
        attempts += 1

        new_status = "LOCKED" if attempts >= 3 else "ACTIVE"

        with get_db() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE mfa_sessions
                SET attempts = ?, status = ?
                WHERE id = ?
            """, (attempts, new_status, session_id))

        return "LOCKED" if new_status == "LOCKED" else "INVALID"

    # Valid OTP
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE mfa_sessions
            SET status = 'VERIFIED'
            WHERE id = ?
        """, (session_id,))

    return "VALID"


@app.route("/")
def home():
    return render_template_string(LOGIN_PAGE)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Validate missing or empty username
    if not username:
        log_login_attempt(username, False)

        return render_template_string(
            LOGIN_PAGE,
            error="Username is required"
        )

    # Validate missing or empty password
    if not password:
        log_login_attempt(username, False)

        return render_template_string(
            LOGIN_PAGE,
            error="Password is required"
        )

    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT password_hash, active
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

    if not user:
        log_login_attempt(username, False)

        return render_template_string(
            LOGIN_PAGE,
            error="Invalid username or password"
        )

    stored_password_hash, active = user

    if not active or hash_password(password) != stored_password_hash:
        log_login_attempt(username, False)

        return render_template_string(
            LOGIN_PAGE,
            error="Invalid username or password"
        )

    log_login_attempt(username, True)

    mfa_session_id, otp = create_mfa_session(username)

    session["mfa_username"] = username
    session["mfa_session_id"] = mfa_session_id
    
    return redirect(url_for("mfa_page"))
    

@app.route("/mfa", methods=["GET"])
def mfa_page():
    username = session.get("mfa_username")

    if not username:
        return redirect(url_for("home"))

    return render_template_string(
        MFA_PAGE,
        username=username
    )
    
@app.route("/resend-mfa", methods=["POST"])
def resend_mfa():
    username = session.get("mfa_username")
    current_session_id = session.get("mfa_session_id")

    if not username or not current_session_id:
        return redirect(url_for("home"))
 
    # Invalidate the current MFA session
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE mfa_sessions
            SET status = 'SUPERSEDED'
            WHERE id = ? AND status = 'ACTIVE'
        """, (current_session_id,))
    
    
    # Create a new MFA session
    new_session_id, otp = create_mfa_session(username)

    # Store the new MFA session ID
    session["mfa_session_id"] = new_session_id

    return render_template_string(
        MFA_PAGE,
        username=username,
        message="A new MFA code has been generated."
    )
    
@app.route("/verify-mfa", methods=["POST"])
def verify_mfa():
   
    username = session.get("mfa_username")
    otp = request.form.get("otp")
    mfa_session_id = session.get("mfa_session_id")
    
    if not username or not mfa_session_id:
        return redirect(url_for("home"))
    
    if not otp:
        return render_template_string(
            MFA_PAGE,
            username=username,
            error="MFA code is required"
        )

    result = verify_mfa_code(mfa_session_id, otp)

    if result == "NOT_FOUND":
        return render_template_string(
            MFA_PAGE,
            username=username,
            error="No active MFA session found"
        )

    if result == "LOCKED":
        return render_template_string(
            MFA_PAGE,
            username=username,
            error="Your MFA session is locked. Please try again later or contact support."
        )

    if result == "ALREADY_VERIFIED":
        return render_template_string(
            MFA_PAGE,
            username=username,
            error="MFA has already been verified."
        )

    if result == "SUPERSEDED":
        return render_template_string(
            MFA_PAGE,
            username=username,
            error="This MFA code is no longer valid. Please use the latest code."
        )

    if result == "EXPIRED":
        return render_template_string(
            MFA_PAGE,
            username=username,
            error="MFA code has expired"
        )

    if result == "INVALID":
        return render_template_string(
            MFA_PAGE,
            username=username,
            error="Invalid MFA code"
        )

    if result == "VALID":
        return """
            <h1>MFA Verification Successful</h1>
            <p id="success-message">
                You have successfully completed Multi-Factor Authentication.
            </p>
        """
        
@app.route("/api/mfa/verify", methods=["POST"])
def api_verify_mfa():
    data = request.get_json() or {}

    mfa_session_id = data.get("mfa_session_id")
    otp = data.get("otp")

    if not mfa_session_id:
        return jsonify({
            "status": "error",
            "message": "MFA session ID is required"
        }), 400

    if not otp:
        return jsonify({
            "status": "error",
            "message": "MFA code is required"
        }), 400

    result = verify_mfa_code(mfa_session_id, otp)

    if result == "NOT_FOUND":
        return jsonify({
            "status": "error",
            "message": "MFA session not found"
        }), 404

    if result == "LOCKED":
        return jsonify({
            "status": "error",
            "message": "MFA session is locked"
        }), 403

    if result == "ALREADY_VERIFIED":
        return jsonify({
            "status": "error",
            "message": "MFA has already been verified"
        }), 409

    if result == "SUPERSEDED":
        return jsonify({
            "status": "error",
            "message": "This MFA code is no longer valid"
        }), 401

    if result == "EXPIRED":
        return jsonify({
            "status": "error",
            "message": "MFA code has expired"
        }), 410

    if result == "INVALID":
        return jsonify({
            "status": "error",
            "message": "Invalid MFA code"
        }), 401

    if result == "VALID":
        return jsonify({
            "status": "success",
            "message": "MFA verification successful"
        }), 200

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    # Validate username
    if not username:
        log_login_attempt(username, False)

        return jsonify({
            "status": "error",
            "message": "Username is required"
        }), 400

    # Validate password
    if not password:
        log_login_attempt(username, False)

        return jsonify({
            "status": "error",
            "message": "Password is required"
        }), 400

    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT password_hash, active
            FROM users
         WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

    # Validate user and password
    if not user:
        log_login_attempt(username, False)

        return jsonify({
            "status": "error",
            "message": "Invalid username or password"
        }), 401

    stored_password_hash, active = user

    if not active or hash_password(password) != stored_password_hash:
        log_login_attempt(username, False)

        return jsonify({
            "status": "error",
            "message": "Invalid username or password"
        }), 401

    # Successful login
    log_login_attempt(username, True)

    return jsonify({
        "status": "success",
        "message": "Valid credentials. MFA required."
    }), 200

if __name__ == "__main__":
    initialize_database()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )