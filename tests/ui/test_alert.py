import json
from pages.login_page import LoginPage
from utils.ui_helpers import handle_dialog


def load_test_data():
    with open("test_data/users.json") as file:
        return json.load(file)


def test_alert_is_handled(page):
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
            "This is a SmartBank test alert"
        )
    )

    page.get_by_role("button", name="Test Alert").click()