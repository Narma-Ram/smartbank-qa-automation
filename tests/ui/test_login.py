import json

from pages.login_page import LoginPage


def load_test_data():
    with open("test_data/users.json") as file:
        return json.load(file)


def test_valid_login_redirects_to_mfa(page):
    test_data = load_test_data()
    valid_user = test_data["valid_user"]

    login_page = LoginPage(page)
    login_page.open("http://127.0.0.1:5000")

    login_page.login(
        valid_user["username"],
        valid_user["password"]
    )

    assert page.locator("h1").inner_text() == \
        "Multi-Factor Authentication"

    assert page.locator("#mfa-message").is_visible()


def test_invalid_login_shows_error(page):
    test_data = load_test_data()
    invalid_user = test_data["invalid_user"]

    login_page = LoginPage(page)
    login_page.open("http://127.0.0.1:5000")

    login_page.login(
        invalid_user["username"],
        invalid_user["password"]
    )

    assert page.locator("#error").is_visible()

    assert page.locator("#error").inner_text() == \
        "Invalid username or password"


def test_inactive_user_cannot_login(page):
    test_data = load_test_data()
    inactive_user = test_data["inactive_user"]

    login_page = LoginPage(page)
    login_page.open("http://127.0.0.1:5000")

    login_page.login(
        inactive_user["username"],
        inactive_user["password"]
    )

    assert page.locator("#error").is_visible()

    assert page.locator("#error").inner_text() == \
        "Invalid username or password"
        
    # Verify inactive user did NOT reach MFA
    assert not page.locator("#mfa-message").is_visible()


def test_missing_username_shows_required_message(page):
    login_page = LoginPage(page)
    login_page.open("http://127.0.0.1:5000")

    page.fill("#password", "ValidPassword123")
    page.click("#login")

    assert page.locator("#error").is_visible()
    assert page.locator("#error").inner_text() == \
        "Username is required"


def test_missing_password_shows_required_message(page):
    login_page = LoginPage(page)
    login_page.open("http://127.0.0.1:5000")

    page.fill("#username", "smartbank_user")
    page.click("#login")

    assert page.locator("#error").is_visible()
    assert page.locator("#error").inner_text() == \
        "Password is required"