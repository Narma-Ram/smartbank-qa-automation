# SmartBank QA Automation

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
