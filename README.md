
# MediPlus Pharmacy API

## Project Overview
MediPlus is a Flask-based pharmacy inventory API developed as a cybersecurity hardening project. It demonstrates authentication, access control, input validation, and protection against repeated login attempts.

## Technologies
- Python 3
- Flask
- PyJWT
- Flask-Limiter
- python-dotenv
- Pytest
- Bandit
- Gunicorn

## Setup

Clone or download the project, then run:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file containing:

```ini
JWT_SECRET=your-long-random-secret
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-strong-password
```

Start the application:

```bash
python app.py
```

The API runs locally at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint | Purpose | Authentication |
|---|---|---|---|
| GET | / | API status | No |
| POST | /login | Obtain JWT | No |
| GET | /medicines | View inventory | Yes |
| POST | /medicines | Add medicine | Yes |
| PUT | /medicines/{id} | Update medicine | Yes |
| DELETE | /medicines/{id} | Delete medicine | Yes |

Protected endpoints require:

`Authorization: Bearer YOUR_TOKEN`

## Security Controls
- JWT-based authentication.
- Protected inventory endpoints.
- Login rate limiting.
- Input validation and rejection of unexpected fields.
- Environment-based credentials and secret configuration.
- Generic error responses.
- Automated testing using Pytest.
- Static security analysis using Bandit.

## Verification

Run automated tests:

```bash
python -m pytest -q
```

Run static security analysis:

```bash
bandit -r app.py
```

## Current Limitations
- Inventory is stored in memory and resets when the application restarts.
- The project uses a single demonstration administrator account.
- A persistent database and production-grade user management are not implemented.
- The Flask development server is intended for local testing, not public production deployment.

## Project Scope
This implementation is a cybersecurity learning prototype and must not be used to store real patient or pharmacy customer information.
