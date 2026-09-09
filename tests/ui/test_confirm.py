import json

from pages.login_page import LoginPage
from utils.ui_helpers import handle_dialog


def load_test_data():
    with open("test_data/users.json") as file:
        return json.load(file)


def test_confirm_dialog_is_dismissed(page):
    test_data = load_test_data()
    valid_user = test_data["valid_user"]

    login_page = LoginPage(page)
    login_page.open("http://127.0.0.1:5000")

    login_page.login(
        valid_user["username"],
        valid_user["password"]
    )

    page.on(
        "dialog",
        lambda dialog: handle_dialog(
            dialog,
            "Do you want to continue?",
            accept=False
        )
    )

    page.get_by_role("button", name="Test Confirm").click()
    assert page.locator("h1").inner_text() == \
        "Multi-Factor Authentication"