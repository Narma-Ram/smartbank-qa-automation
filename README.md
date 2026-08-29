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



