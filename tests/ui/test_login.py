import json
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage


def load_test_data():
    with open("test_data/users.json") as file:
        return json.load(file)


def test_valid_login_redirects_to_mfa():
    test_data = load_test_data()
    valid_user = test_data["valid_user"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login_page = LoginPage(page)
        login_page.open("http://127.0.0.1:5000")

        login_page.login(
            valid_user["username"],
            valid_user["password"]
        )

        assert page.locator("h1").inner_text() == \
            "Multi-Factor Authentication"

        assert page.locator("#mfa-message").is_visible()

        browser.close()


def test_invalid_login_shows_error():
    test_data = load_test_data()
    invalid_user = test_data["invalid_user"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login_page = LoginPage(page)
        login_page.open("http://127.0.0.1:5000")

        login_page.login(
            invalid_user["username"],
            invalid_user["password"]
        )

        assert page.locator("#error").is_visible()

        assert page.locator("#error").inner_text() == \
            "Invalid username or password"

        browser.close()


def test_inactive_user_cannot_login():
    test_data = load_test_data()
    inactive_user = test_data["inactive_user"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

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

        browser.close()