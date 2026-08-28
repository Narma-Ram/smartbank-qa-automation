from flask import Flask, request, jsonify, render_template_string
import hashlib
import sqlite3
from datetime import datetime


app = Flask(__name__)

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

    <label for="otp">MFA Code</label>
    <input id="otp" type="text">

    <button id="verify-mfa">Verify</button>
</body>
</html>
"""


def get_connection():
    return sqlite3.connect(DB_NAME)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


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
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO login_audit
        (username, success, attempt_time)
        VALUES (?, ?, ?)
    """, (
        username,
        success,
        datetime.now().isoformat()
    ))

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template_string(LOGIN_PAGE)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT password_hash, active
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    connection.close()

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

    return render_template_string(MFA_PAGE)


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

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT password_hash, active
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    connection.close()

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