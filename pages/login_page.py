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
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()