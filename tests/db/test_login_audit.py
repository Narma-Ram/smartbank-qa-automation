import sqlite3
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
import requests


DB_NAME = "smartbank.db"


def get_latest_audit_record(username):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT username, success, attempt_time
        FROM login_audit
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 1
    """, (username,))

    record = cursor.fetchone()
    connection.close()

    return record


def test_successful_login_creates_audit_record():

    # Step 1: Perform a fresh login through the UI
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        login_page = LoginPage(page)

        login_page.open("http://127.0.0.1:5000")

        login_page.login(
            "smartbank_user",
            "ValidPassword123"
        )

        # Verify login reached MFA
        assert page.locator("#mfa-message").is_visible()

        browser.close()

    # Step 2: Check the database audit log
    record = get_latest_audit_record("smartbank_user")

    # Step 3: Verify the audit record
    assert record is not None

    username, success, attempt_time = record

    assert username == "smartbank_user"
    assert success == 1
    assert attempt_time is not None
    
def test_api_login_creates_audit_record():
    # Step 1: Perform login through API
    response = requests.post(
        "http://127.0.0.1:5000/api/login",
        json={
            "username": "smartbank_user",
            "password": "ValidPassword123"
        }
    )

    # Verify API response
    assert response.status_code == 200

    # Step 2: Get latest audit record from database
    record = get_latest_audit_record("smartbank_user")

    # Step 3: Verify database record
    assert record is not None

    username, success, attempt_time = record

    assert username == "smartbank_user"
    assert success == 1
    assert attempt_time is not None
