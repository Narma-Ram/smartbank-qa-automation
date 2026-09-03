import sqlite3
from datetime import datetime, timedelta
import requests

from conftest import db_connection


BASE_URL = "http://127.0.0.1:5000"
DB_NAME = "smartbank.db"


def create_test_mfa_session():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, otp_code
        FROM mfa_sessions
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 1
    """, ("smartbank_user",))

    session_data = cursor.fetchone()
    connection.close()

    return session_data


import requests

BASE_URL = "http://127.0.0.1:5000"


def test_valid_mfa_api(mfa_session ,db_connection):
    session_id = mfa_session["session_id"]
    otp = mfa_session["otp"]

    response = requests.post(
        f"{BASE_URL}/api/mfa/verify",
        json={
            "mfa_session_id": session_id,
            "otp": otp
        }
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["status"] == "success"
    assert response_body["message"] == "MFA verification successful"
    
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT status
        FROM mfa_sessions
        WHERE id = ?
    """, (session_id,))

    status = cursor.fetchone()[0]
    #print("Database MFA status:", status)
    assert status == "VERIFIED"
    
def test_invalid_mfa_api(mfa_session, db_connection):
    session_id = mfa_session["session_id"]
    correct_otp = mfa_session["otp"]

    wrong_otp = "000000"

    # Make sure our test OTP is actually different
    assert wrong_otp != correct_otp

    response = requests.post(
        f"{BASE_URL}/api/mfa/verify",
        json={
            "mfa_session_id": session_id,
            "otp": wrong_otp
        }
    )

    assert response.status_code == 401

    response_body = response.json()

    assert response_body["status"] == "error"
    assert response_body["message"] == "Invalid MFA code"

    # Verify database state
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT attempts, status
        FROM mfa_sessions
        WHERE id = ?
    """, (session_id,))

    attempts, status = cursor.fetchone()

    assert attempts == 1
    assert status == "ACTIVE"
    
def test_mfa_lockout_after_three_invalid_attempts(mfa_session, db_connection):
    session_id = mfa_session["session_id"]
    correct_otp = mfa_session["otp"]

    wrong_otp = "000000"
    assert wrong_otp != correct_otp

    # Attempt 1
    response = requests.post(
        f"{BASE_URL}/api/mfa/verify",
        json={
            "mfa_session_id": session_id,
            "otp": wrong_otp
        }
    )

    assert response.status_code == 401

    # Attempt 2
    response = requests.post(
        f"{BASE_URL}/api/mfa/verify",
        json={
            "mfa_session_id": session_id,
            "otp": wrong_otp
        }
    )

    assert response.status_code == 401

    # Attempt 3
    response = requests.post(
        f"{BASE_URL}/api/mfa/verify",
        json={
            "mfa_session_id": session_id,
            "otp": wrong_otp
        }
    )

    assert response.status_code == 403

    response_body = response.json()

    assert response_body["status"] == "error"
    assert response_body["message"] == "MFA session is locked"

    # Verify database state
    cursor = db_connection.cursor()

    cursor.execute("""
        SELECT attempts, status
        FROM mfa_sessions
        WHERE id = ?
    """, (session_id,))

    attempts, status = cursor.fetchone()

    assert attempts == 3
    assert status == "LOCKED"
    
def test_expired_mfa_api(mfa_session, db_connection):
    session_id = mfa_session["session_id"]
    otp = mfa_session["otp"]

    # Make the MFA session expired
    cursor = db_connection.cursor()

    expired_time = (datetime.now() - timedelta(minutes=1)).isoformat()

    cursor.execute("""
        UPDATE mfa_sessions
        SET expiry_time = ?
        WHERE id = ?
    """, (expired_time, session_id))

    db_connection.commit()

    # Verify expired OTP through API
    response = requests.post(
        f"{BASE_URL}/api/mfa/verify",
        json={
            "mfa_session_id": session_id,
            "otp": otp
        }
    )

    assert response.status_code == 410

    response_body = response.json()

    assert response_body["status"] == "error"
    assert response_body["message"] == "MFA code has expired"
    
def test_missing_mfa_session_id():
    response = requests.post(
        f"{BASE_URL}/api/mfa/verify",
        json={
            "otp": "123456"
        }
    )

    assert response.status_code == 400

    response_body = response.json()

    assert response_body["status"] == "error"
    assert response_body["message"] == "MFA session ID is required"
    
def test_missing_otp():
    response = requests.post(
        f"{BASE_URL}/api/mfa/verify",
        json={
            "mfa_session_id": 123
        }
    )

    assert response.status_code == 400

    response_body = response.json()

    assert response_body["status"] == "error"
    assert response_body["message"] == "MFA code is required"