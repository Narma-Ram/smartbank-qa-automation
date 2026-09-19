# SmartBank QA Automation — CI/CD Guide

## 1. Overview

The SmartBank QA Automation project uses Continuous Integration (CI) to automatically validate the application through automated UI, API, and database tests.

The project currently supports two CI environments:

- GitHub Actions
- Jenkins

Both environments use Python, pytest, and Playwright to execute the automated test suite.
## 2. GitHub Actions

GitHub Actions is used to automatically execute the SmartBank automated test suite when changes are pushed to the `main` branch or when a pull request is created.

### CI Workflow

The GitHub Actions workflow performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs the project dependencies from `requirements.txt`.
4. Installs the Chromium, Firefox, and WebKit Playwright browsers.
5. Starts the SmartBank Flask application.
6. Executes the pytest test suite.
7. Generates a self-contained HTML test report.
8. Uploads the HTML report as a GitHub Actions artifact.
9. Uploads failure screenshots when the test job fails.

### Browser Coverage

The Playwright test framework supports:

- Chromium
- Firefox
- WebKit

The current GitHub Actions workflow executes the complete test suite sequentially. Parallel execution with `pytest-xdist` is currently used for local testing rather than CI.

### GitHub Actions Result

The CI pipeline successfully executes the complete automated test suite.

The current regression suite contains:

- UI tests
- API tests
- Database tests

The latest successful CI execution completed with:

**40 tests passed.**
## 3. Jenkins

Jenkins is used as a second CI environment for the SmartBank QA Automation project.

The Jenkins job is configured as a Freestyle project named:

`SmartBank-QA-Automation`

The job retrieves the project from the GitHub repository and executes the automated test suite on a Windows 11 environment.

### Jenkins Environment

The Jenkins environment uses:

- Windows 11 Pro
- Java 21
- Python 3.12
- Git
- pytest
- Playwright
- Flask
- SQLite

### Jenkins Build Process

The Jenkins build performs the following steps:

1. Checks out the `main` branch from GitHub.
2. Installs Python dependencies from `requirements.txt`.
3. Initializes the SmartBank SQLite database.
4. Installs Chromium, Firefox, and WebKit Playwright browsers.
5. Starts the SmartBank Flask application.
6. Executes the complete pytest test suite.

The Jenkins build currently runs the tests sequentially.

### Jenkins Test Result

The Jenkins pipeline successfully executes the complete automated regression suite.

Latest verified result:

**40 tests passed in approximately 12.5 seconds.**

The test suite covers:

- UI testing
- API testing
- Database testing
- Chromium
- Firefox
- WebKit

### Jenkins Job Configuration

The Jenkins Freestyle project uses the following configuration.

**Source Code Management**

- SCM: Git
- Repository: SmartBank QA Automation GitHub repository
- Branch: `*/main`

**Build Trigger**

- Manual build trigger is currently used.
- Automatic triggers can be added later if required.

**Build Steps**

The Jenkins build executes the following commands:

```text
python -m pip install -r requirements.txt

python -c "from app.app import initialize_database; initialize_database()"

python -m playwright install chromium firefox webkit

Start SmartBank Flask application

python -m pytest tests -v

## 4. Local Parallel Test Execution

The project uses `pytest-xdist` to support parallel execution of Playwright UI tests during local development.

The UI test suite is configured to run across:

- Chromium
- Firefox
- WebKit

The following command runs the UI tests using three parallel workers:

```text
pytest -v tests/ui -n 3