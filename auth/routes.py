# The auth department — handles signup AND login
# Doesn't know about bookmarks. Just user accounts.

from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from models import db, User

import jwt
# JWT (JSON Web Token) creates tokens — small encoded strings
# that prove who you are. Like a concert wristband.

import datetime
# We need this to set when the token expires

auth_bp = Blueprint("auth", __name__)
# The auth department

bcrypt = Bcrypt()
# Password scrambling tool

SECRET_KEY = "your-secret-key-change-this-later"
# This is the "master password" used to create and verify tokens
# Only our server knows this key
# If someone doesn't know this key, they can't fake a token
# In a real app you'd hide this in an environment variable


# -------- SIGNUP (same as before, no changes) --------

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


# -------- LOGIN (new) --------
# The user sends username + password
# We verify them and give back a token
#
# curl -X POST http://127.0.0.1:8000/login
#   -H "Content-Type: application/json"
#   -d '{"username": "kaizen", "password": "mypassword123"}'

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    # --- VALIDATION ---
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    # --- FIND THE USER ---
    user = User.query.filter_by(username=data["username"]).first()
    # Search the database for this username
    # Returns the User object if found, None if not

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401
        # 401 = "unauthorized" — you failed to prove who you are
        # We DON'T say "user not found" — that tells hackers
        # which usernames exist. We keep the message vague on purpose.

    # --- CHECK THE PASSWORD ---
    if not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401
    # Here's what this does step by step:
    # 1. Takes the password the client sent: "mypassword123"
    # 2. Scrambles it the same way we scrambled it during signup
    # 3. Compares the new scramble to the scramble stored in the database
    # 4. If they match → password is correct
    # 5. If they don't match → wrong password
    #
    # We NEVER unscramble the stored password
    # We scramble the new one and compare the two scrambles

    # --- CREATE A TOKEN ---
    token = jwt.encode(
        {
            "user_id": user.id,
            # So we know WHO this token belongs to

            "username": user.username,
            # For convenience — we can read the username from the token

            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            # Token expires in 24 hours
            # After that, the user has to log in again
            # This is a security measure — stolen tokens don't last forever
        },
        SECRET_KEY,
        # The master password used to sign the token
        # Without this key, nobody can create a valid token

        algorithm="HS256"
        # The method used to sign the token — standard, don't overthink it
    )
    # token is now a long string like "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
    # It looks random but it actually contains the user_id, username,
    # and expiration — encoded (not encrypted, encoded)
    # Anyone can READ a token, but only our server can CREATE a valid one
    # because only we know the SECRET_KEY

    return jsonify({"token": token, "username": user.username})
    # Send the token back to the client
    # From now on, the client includes this token in every request
    # instead of sending their password every time
'''

Replace your `auth/routes.py` with this. Your other three files stay exactly the same. Then:
```
rm -f bookmarks.db
/Users/aman.shrestha_003/Backend/Backend-/.venv/bin/python app.py
```

In Tab 2:
```
curl -X POST http://127.0.0.1:8000/signup -H "Content-Type: application/json" -d '{"username": "kaizen", "password": "mypassword123"}'
```
```
curl -X POST http://127.0.0.1:8000/login -H "Content-Type: application/json" -d '{"username": "kaizen", "password": "mypassword123"}'
'''