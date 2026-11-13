
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

## Deployment

The MediPlus API was deployed on an Ubuntu Server 22.04 virtual machine.

### Deployment architecture

Client → Nginx (HTTPS, port 443) → Gunicorn (127.0.0.1:8000) → Flask API

### Services
- **Nginx:** Reverse proxy, HTTP-to-HTTPS redirection and security response headers.
- **Gunicorn:** WSGI application server managed by systemd.
- **Flask:** Handles API routes, JWT authentication and medicine operations.
- **UFW:** Allows SSH (22), HTTP (80) and HTTPS (443).
- **Fail2ban:** Protects SSH against repeated failed login attempts.

### HTTPS configuration

A self-signed TLS certificate was generated for the local lab environment. TLS 1.2 and TLS 1.3 are enabled. The certificate is not publicly trusted.

For local testing:

```bash
curl -k https://127.0.0.1/
```

The `-k` option is used only because the lab certificate is self-signed. A production deployment should use a trusted certificate and a public domain.

### Verification

- Automated tests: 11 passed.
- Bandit static security analysis: no issues identified.
- HTTPS health endpoint: HTTP 200.
- Unauthenticated medicine endpoint: HTTP 401.
- HTTP requests redirect to HTTPS.
- Nginx configuration test: successful.

### Limitations

- Medicine records are stored in memory and are not persistent.
- A single Gunicorn worker is used to avoid separate in-memory inventories between workers.
- The project uses a single demonstration administrator account.
- Rate limiting uses in-memory storage.
- The TLS certificate is self-signed and intended for local lab use.
- The VM does not have a public IP address or domain, so the service is not publicly accessible.
- The project is a security demonstration, not a production pharmacy system.
