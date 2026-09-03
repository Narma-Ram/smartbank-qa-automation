import base64
import platform
from pathlib import Path
from app.app import create_mfa_session
import sqlite3
import pytest
from pytest_metadata.plugin import metadata_key

from playwright.sync_api import sync_playwright


def pytest_configure(config):
    config.stash[metadata_key]["Project"] = "SmartBank QA Automation"
    config.stash[metadata_key]["Test Type"] = "UI, API, and Database Testing"
    config.stash[metadata_key]["Environment"] = "Local / GitHub Actions CI"
    config.stash[metadata_key]["Python Version"] = platform.python_version()


def pytest_html_report_title(report):
    report.title = "SmartBank QA Automation Test Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page:
            screenshot_dir = Path("reports/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            screenshot_path = screenshot_dir / f"{item.name}.png"

            page.screenshot(
                path=str(screenshot_path),
                full_page=True
            )

            screenshot_base64 = base64.b64encode(
                screenshot_path.read_bytes()
            ).decode("utf-8")

            pytest_html = item.config.pluginmanager.getplugin("html")

            if pytest_html:
                extra = getattr(report, "extras", [])

                extra.append(
                    pytest_html.extras.image(
                        screenshot_base64,
                        mime_type="image/png",
                        extension="png"
                    )
                )

                report.extras = extra
            
@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        yield page

        browser.close()
        
@pytest.fixture        
def mfa_session():
    session_id, otp = create_mfa_session("smartbank_user")

    return {
        "session_id": session_id,
        "otp": otp
    }
    
@pytest.fixture
def db_connection():
    connection = sqlite3.connect("smartbank.db")
    yield connection
    connection.close()