# MediPlus Pharmacy API

[![MediPlus Security Checks](https://github.com/shzaibr/mediplus-pharmacy-api/actions/workflows/security.yml/badge.svg)](https://github.com/shzaibr/mediplus-pharmacy-api/actions/workflows/security.yml)

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

For local development only, `python app.py` starts the Flask development server at `http://127.0.0.1:5000`. The public deployment is hosted on PythonAnywhere over HTTPS.

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

### Public Deployment: PythonAnywhere

**Live API URL:** https://shzaibr.pythonanywhere.com/

MediPlus is publicly deployed on PythonAnywhere using a manually configured Flask WSGI application. The Ubuntu VM described below is used for local security testing and host-hardening exercises, not public hosting.

### Hosting Configuration

- Hosting platform: PythonAnywhere
- Python runtime: 3.10.12
- Framework: Flask 3.1.3
- Application entry point: Flask WSGI application
- Virtual environment: `/home/shzaibr/.virtualenvs/mediplus-venv`
- Project directory: `/home/shzaibr/mediplus-pharmacy-api`
- WSGI configuration: `/var/www/shzaibr_pythonanywhere_com_wsgi.py`
- Public protocol: HTTPS
- Production credentials: Stored in a private `.env` file with permissions `0600`; excluded from Git.

### Deployment Architecture

Client -> HTTPS -> PythonAnywhere WSGI hosting -> Flask API -> Medicine inventory

PythonAnywhere uses the platform-provided `X-Real-IP` header for client identification in rate limiting and security-event logging. The Ubuntu VM configuration retains its separate trusted Nginx ProxyFix handling.

### Live API Verification

The following checks were performed against the publicly accessible PythonAnywhere deployment:

- API health endpoint: HTTP 200.
- Unauthenticated medicine request: HTTP 401.
- Administrator login: HTTP 200; JWT issued.
- Authenticated medicine retrieval: HTTP 200.
- Medicine creation: HTTP 201.
- Medicine update: HTTP 200.
- Medicine deletion: HTTP 200.
- Unsupported HTTP method: HTTP 405 with JSON response.

The temporary medicine used for CRUD verification was deleted successfully.

### Automated Security Verification

- Pytest regression suite: 11 tests passed.
- Bandit: no issues identified at the configured severity threshold.
- GitHub Actions runs Bandit and Pytest on pushes and pull requests.

Workflow: https://github.com/shzaibr/mediplus-pharmacy-api/actions

Live deployment: https://shzaibr.pythonanywhere.com/

### Deployment Limitations

- Medicine records are stored in memory and reset when the application reloads.
- The project uses a single demonstration administrator account.
- Rate limiting uses in-memory storage.
- The application is a cybersecurity learning prototype, not a production pharmacy system.
- The Ubuntu VM is a separate local testing environment and is not the public API host.

## Ubuntu VM Host Hardening and Service Management

### Firewall
- UFW is enabled with incoming traffic denied by default.
- Only SSH (22/tcp) and HTTP (80/tcp) are allowed inbound for IPv4 and IPv6.

### SSH security
- Root login is disabled.
- Password and keyboard-interactive authentication are disabled.
- Public-key authentication is required for remote administration.

### Service minimization
The following services were stopped and masked to reduce the attack surface:
- Avahi: local network discovery is not required.
- CUPS and CUPS-Browsed: printing is not required.
- Colord: display colour-profile management is not required.
- PackageKit: graphical package management is not required; command-line APT remains available.
- Power Profiles and Switcheroo Control: desktop power-profile and GPU switching are unnecessary.
- Multipath: multipath storage is not configured.
- WPA Supplicant: wireless authentication is not required for this wired VM.
- LightDM: masked to keep the VM headless.
- TTY1 Getty: masked to disable local TTY1 login while SSH is used for administration.

The individual retention reasons for all running services are documented in `evidence/running_services.txt`.

XFCE remains installed. To restore the graphical desktop when required, run `sudo systemctl unmask lightdm.service` followed by `sudo systemctl start lightdm.service`.
