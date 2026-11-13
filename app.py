
import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("JWT_SECRET", "")
app.config["JWT_ALGORITHM"] = "HS256"

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"],
    storage_uri="memory://",
)


# Demo inventory: data is stored in memory and resets on restart.
medicines = {
    1: {"id": 1, "name": "Paracetamol", "quantity": 100, "price": 2.50},
    2: {"id": 2, "name": "Cetirizine", "quantity": 50, "price": 3.00},
    3: {"id": 3, "name": "Vitamin C", "quantity": 75, "price": 5.00},
}


def create_token(username):
    expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {"sub": username, "exp": expiry}
    return jwt.encode(
        payload,
        app.config["SECRET_KEY"],
        algorithm=app.config["JWT_ALGORITHM"],
    )


def token_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Authentication token required"}), 401

        try:
            payload = jwt.decode(
                parts[1],
                app.config["SECRET_KEY"],
                algorithms=[app.config["JWT_ALGORITHM"]],
            )
            request.current_user = payload["sub"]
        except (jwt.InvalidTokenError, KeyError):
            return jsonify({"error": "Invalid or expired token"}), 401

        return function(*args, **kwargs)

    return wrapper


def validate_medicine(data, partial=False):
    if not isinstance(data, dict):
        return "Request body must be a JSON object"

    allowed = {"name", "quantity", "price"}
    if set(data) - allowed:
        return "Unexpected field in request"

    required = allowed if not partial else set(data)
    if not partial and not required.issubset(data):
        return "Name, quantity and price are required"

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return "Name must be a non-empty string"
        if len(data["name"].strip()) > 100:
            return "Name must not exceed 100 characters"

    if "quantity" in data:
        value = data["quantity"]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            return "Quantity must be a non-negative integer"

    if "price" in data:
        value = data["price"]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            return "Price must be a non-negative number"

    return None


@app.get("/")
def home():
    return jsonify({
        "message": "MediPlus Pharmacy API",
        "status": "running"
    })


@app.post("/login")
@limiter.limit("5 per minute")
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON username and password required"}), 400

    username = os.getenv("ADMIN_USERNAME", "")
    password = os.getenv("ADMIN_PASSWORD", "")

    if (
        not username
        or not password
        or data.get("username") != username
        or data.get("password") != password
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"access_token": create_token(username)}), 200


@app.get("/medicines")
@token_required
def get_medicines():
    return jsonify(list(medicines.values())), 200


@app.post("/medicines")
@token_required
def add_medicine():
    data = request.get_json(silent=True)
    error = validate_medicine(data)

    if error:
        return jsonify({"error": error}), 400

    new_id = max(medicines.keys(), default=0) + 1
    medicine = {
        "id": new_id,
        "name": data["name"].strip(),
        "quantity": data["quantity"],
        "price": float(data["price"]),
    }
    medicines[new_id] = medicine

    return jsonify(medicine), 201


@app.put("/medicines/<int:medicine_id>")
@token_required
def update_medicine(medicine_id):
    if medicine_id not in medicines:
        return jsonify({"error": "Medicine not found"}), 404

    data = request.get_json(silent=True)
    error = validate_medicine(data, partial=True)

    if error:
        return jsonify({"error": error}), 400

    if not data:
        return jsonify({"error": "At least one field is required"}), 400

    medicine = medicines[medicine_id]
    for field, value in data.items():
        medicine[field] = value.strip() if field == "name" else value

    medicine["price"] = float(medicine["price"])
    return jsonify(medicine), 200


@app.delete("/medicines/<int:medicine_id>")
@token_required
def delete_medicine(medicine_id):
    if medicine_id not in medicines:
        return jsonify({"error": "Medicine not found"}), 404

    del medicines[medicine_id]
    return jsonify({"message": "Medicine deleted"}), 200


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(429)
def too_many_requests(_error):
    return jsonify({"error": "Too many requests; try again later"}), 429


@app.errorhandler(500)
def internal_error(_error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

