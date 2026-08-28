import requests
BASE_URL = "http://127.0.0.1:5000"


def test_valid_api_login():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "username": "smartbank_user",
            "password": "ValidPassword123"
        }
    )

    assert response.status_code == 200
    response_body = response.json()

    assert response_body["status"] == "success"
    assert response_body["message"] == "Valid credentials. MFA required."


def test_invalid_api_login():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "username": "invalid_user",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401
    response_body = response.json()

    assert response_body["status"] == "error"
    assert response_body["message"] == "Invalid username or password"


def test_missing_username():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "password": "ValidPassword123"
        }
    )

    assert response.status_code == 400
    response_body = response.json()

    assert response_body["status"] == "error"
    assert response_body["message"] == "Username is required"

def test_missing_password():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "username": "smartbank_user"
        }
    )

    assert response.status_code == 400
    response_body = response.json()

    assert response_body["status"] == "error"
    assert response_body["message"] == "Password is required"

def test_empty_username_and_password():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "username": "",
            "password": ""
        }
    )

    assert response.status_code == 400
    response_body = response.json()

    assert response_body["status"] == "error"
    assert response_body["message"] == "Username is required"

def test_very_long_username():
    long_username = "a" * 1000

    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "username": long_username,
            "password": "ValidPassword123"
        }
    )

    assert response.status_code == 401

    response_body = response.json()

    assert response_body["status"] == "error"
    assert "password" not in response_body
    
def test_sql_injection_like_input():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "username": "' OR '1'='1",
            "password": "' OR '1'='1"
        }
    )

    assert response.status_code == 401
    response_body = response.json()

    assert response_body["status"] == "error"
    assert response_body["message"] == "Invalid username or password"
    
def test_special_characters_in_credentials():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "username": "@#$%^&*!",
            "password": "!@#$%^&*()"
        }
    )

    assert response.status_code == 401
    assert response.json()["status"] == "error"