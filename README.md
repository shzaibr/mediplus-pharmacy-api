
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

The MediPlus API is deployed on an Ubuntu Server 22.04 virtual machine.

### Deployment architecture

Client → Nginx (HTTP, port 80) → Gunicorn (127.0.0.1:8000) → Flask API

### Services

- **Nginx:** HTTP reverse proxy on port 80, forwarding requests to Gunicorn and adding security response headers.
- **Gunicorn:** WSGI application server managed by systemd.
- **Flask:** Handles API routes, JWT authentication and medicine operations.
- **UFW:** Allows inbound SSH (22/tcp) and HTTP (80/tcp) only, for IPv4 and IPv6. Incoming traffic is denied by default.
- **Fail2ban:** Protects SSH against repeated failed login attempts.

### HTTP configuration

Nginx listens on port 80 for IPv4 and IPv6 and forwards requests to Gunicorn at 127.0.0.1:8000. The reverse proxy adds X-Content-Type-Options, X-Frame-Options and Referrer-Policy security headers.

The current deployment uses unencrypted HTTP only. No HTTPS listener, TLS configuration or HTTP-to-HTTPS redirect is configured.

### Verification

- Automated tests: 11 passed.
- Bandit static security analysis: no issues identified.
- HTTP health endpoint: HTTP 200.
- Unauthenticated medicine endpoint: HTTP 401.
- Nginx configuration test: successful.
- Nginx verified to listen on port 80 only.

### Limitations

- Medicine records are stored in memory and reset when the application restarts.
- The project uses a single demonstration administrator account.
- Rate limiting uses in-memory storage.
- HTTP traffic is unencrypted and should only be used in this controlled lab environment.
- The VM does not have a public IP address or domain, so the service is not publicly accessible.
- The project is a cybersecurity demonstration, not a production pharmacy system.

## Host Hardening and Service Management

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
