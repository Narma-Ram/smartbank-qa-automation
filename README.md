# SmartBank QA Automation
End-to-end QA automation project demonstrating UI automation, API testing, database validation, and CI/CD.

## Project Overview
This project demonstrates an automated testing framework for a SmartBank login application.

The login workflow includes:
- Valid and invalid user authentication
- Inactive user validation
- Password masking
- Multi-Factor Authentication (MFA) redirection
- API login validation
- Input validation for missing and empty credentials
- Long username validation
- SQL injection-like input testing
- Special character validation
- Database audit log validation

## Technologies Used
- Python
- Pytest
- Playwright
- Requests
- Flask
- SQLite
- Git
- GitHub
- GitHub Actions

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
│   ├── db/
│   │   └── test_login_audit.py
│   └── ui/
│       ├── test_login.py
│       └── test_password_masking.py
│
├── docs/
│   ├── requirements/
│   └── test-cases/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── requirements.txt
└── README.md
