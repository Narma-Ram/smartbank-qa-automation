from pages.login_page import LoginPage


def test_password_is_masked(page):
    login_page = LoginPage(page)
    login_page.open("http://127.0.0.1:5000")

    password_field = page.locator("#password")

    assert password_field.get_attribute("type") == "password"