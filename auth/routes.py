from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from models import db, User
import jwt
import datetime

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()
SECRET_KEY = "your-secret-key-change-this-later"

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400
    if len(data["username"]) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400
    if len(data["password"]) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"error": "Username already taken"}), 409
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(username=data["username"], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Account created", "username": user.username}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400
    user = User.query.filter_by(username=data["username"]).first()
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401
    if not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401
    token = jwt.encode(
        {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return jsonify({"token": token, "username": user.username})
