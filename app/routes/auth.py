from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from ..extensions import db
from ..models import User


auth_bp = Blueprint("auth", __name__)


def _parse_payload() -> tuple[dict, tuple[dict, int] | None]:
    if not request.is_json:
        return {}, ({"error": "Request must be JSON"}, 400)

    payload = request.get_json(silent=True) or {}
    return payload, None


@auth_bp.post("/register")
def register():
    payload, error = _parse_payload()
    if error:
        return error

    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", ""))
    email = str(payload.get("email", "")).strip().lower() or None

    if not username:
        return jsonify({"error": "Username is required"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    if email and User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Account created", "user": user.to_public_dict()}), 201


@auth_bp.post("/login")
def login():
    payload, error = _parse_payload()
    if error:
        return error

    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", ""))

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token, "user": user.to_public_dict()}), 200


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": user.to_public_dict()}), 200
