from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage


def test_password_is_masked():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        login_page = LoginPage(page)
        login_page.open("http://127.0.0.1:5000")

        password_field = page.locator("#password")

        assert password_field.get_attribute("type") == "password"

        browser.close()
