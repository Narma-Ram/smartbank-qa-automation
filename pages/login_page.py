from utils.ui_helpers import click_element, fill_input

class LoginPage:

    def __init__(self, page):
        self.page = page

        # Locators
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login")

    def open(self, url):
        self.page.goto(url)

    def login(self, username, password):
        fill_input(self.username_input, username)
        fill_input(self.password_input, password)
        click_element(self.login_button)