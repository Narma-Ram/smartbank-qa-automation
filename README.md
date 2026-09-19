# SmartBank QA Automation

![SmartBank QA Automation](https://github.com/Narma-Ram/smartbank-qa-automation/actions/workflows/ci.yml/badge.svg)

End-to-end QA automation project demonstrating UI automation, API testing, database validation, test reporting, and CI/CD.

## Project Overview

This project demonstrates an automated testing framework for a SmartBank login application.

The framework validates the application across multiple layers:

- UI testing
- API testing
- Database validation
- Automated test reporting
- Continuous Integration with GitHub Actions

## Test Coverage

The automated test suite currently includes **16 tests** covering:

### UI Testing

- Valid user authentication
- Invalid user authentication
- Inactive user validation
- Missing username validation
- Missing password validation
- Password masking
- Multi-Factor Authentication (MFA) redirection

### API Testing

- Valid API login
- Invalid API login
- Missing username
- Missing password
- Empty username and password
- Long username validation
- SQL injection-like input testing
- Special character validation

### Database Testing

- Successful login audit record validation
- API login audit record validation

## Technologies Used

- Python
- Pytest
- Playwright
- Requests
- Flask
- SQLite
- pytest-html
- Git
- GitHub
- GitHub Actions

## Test Automation Features

- Page Object Model (POM)
- JSON-based test data
- Shared Pytest fixtures
- UI, API, and database testing
- Automated HTML test reports
- Custom test report metadata
- Automatic screenshots for failed UI tests
- Failure screenshots embedded in HTML reports
- GitHub Actions CI pipeline
- Test reports uploaded as GitHub Actions artifacts

## Project Structure

```text
smartbank-qa-automation/
│
├── app/
│   └── app.py
│
├── pages/
│   └── login_page.py
│
├── test_data/
│   └── users.json
│
├── tests/
│   ├── api/
│   │   └── test_login_api.py
│   │
│   ├── db/
│   │   └── test_login_audit.py
│   │
│   └── ui/
│       ├── test_login.py
│       └── test_password_masking.py
│
├── reports/
│   └── screenshots/
│
├── docs/
│   ├── requirements/
│   └── test-cases/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── conftest.py
├── requirements.txt
└── README.md

</>Markdown
###  Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/Narma-Ram/smartbank-qa-automation.git
cd smartbank-qa-automation
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright

```bash
python -m playwright install chromium
```

### 5. Start the SmartBank application

```bash
python app/app.py
```

### 6. Run the automated tests

Open another terminal and run:

```bash
python -m pytest tests -v
```

## Generate an HTML Test Report

```bash
python -m pytest tests -v --html=reports/report.html --self-contained-html
```

The HTML report includes:

- Test execution summary
- Pass and fail results
- Project metadata
- Environment information
- Failure details
- Screenshots for failed UI tests

## Continuous Integration

The project uses GitHub Actions to automatically:

1. Check out the source code
2. Set up Python
3. Install project dependencies
4. Install the Playwright Chromium browser
5. Start the SmartBank application
6. Run the automated test suite
7. Generate an HTML test report
8. Upload the test report as a GitHub Actions artifact
9. Upload failure screenshots when a test failure occurs

The workflow runs automatically on:

- Pushes to the `main` branch
- Pull requests targeting the `main` branch

## CI/CD Workflow

```text
Code Push
    ↓
GitHub Actions
    ↓
Install Dependencies
    ↓
Install Playwright
    ↓
Start SmartBank Application
    ↓
Run UI + API + Database Tests
    ↓
Generate HTML Report
    ↓
Capture Failure Screenshots
    ↓
Upload Test Artifacts
```

## Author

**Narma Ram**

QA Automation Engineer | Software Quality Assurance

---

This project demonstrates hands-on experience with automated UI testing, API testing, database validation, test reporting, and CI/CD using modern QA automation tools.


## 🎉 Sprint 1 – Completed

✅ Requirements and acceptance criteria

✅ QA test planning and test cases

✅ UI automation with Playwright

✅ API testing

✅ Database validation

✅ 16 automated tests

✅ Page Object Model (POM)

✅ JSON-based test data

✅ Shared Pytest fixtures

✅ HTML test reporting

✅ Custom test report metadata

✅ Automatic failure screenshots

✅ Failure screenshots embedded in HTML reports

✅ GitHub Actions CI pipeline

✅ GitHub Actions test-report artifacts

✅ Professional project README

✅ GitHub Actions status badge

✅ Clean Git working tree


## 🎉 Sprint 2 – Completed

✅ Secure Multi-Factor Authentication (MFA) requirements and acceptance criteria  
✅ MFA QA test planning and test cases  
✅ MFA UI automation with Playwright  
✅ MFA API endpoint implementation  
✅ Postman API testing  
✅ Valid MFA OTP validation  
✅ Invalid MFA OTP validation  
✅ MFA OTP expiration validation  
✅ 3-attempt MFA lockout validation  
✅ Correct OTP rejected after lockout  
✅ MFA session resend / superseded OTP validation  
✅ API + Database validation  
✅ Automated MFA API tests  
✅ 22 automated tests  
✅ Shared Pytest fixtures  
✅ Reusable database connection fixture  
✅ HTML test reporting  
✅ Custom test report metadata  
✅ Automatic failure screenshots  
✅ Failure screenshots embedded in HTML reports  
✅ GitHub Actions CI pipeline  
✅ GitHub Actions test-report artifacts  
✅ GitHub Actions status badge  
✅ GitHub repository documentation  
✅ Clean Git working tree

### Sprint 2 – Key Achievement

Built and automated a secure MFA workflow with OTP generation, expiration,
attempt tracking, 3-attempt lockout, session replacement, API validation,
and database verification.

**Regression result: 22 tests passed ✅**

## 🎉 Sprint 3 – Completed
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


