from flask import request
import jwt

SECRET_KEY = "your-secret-key-change-this-later"

def get_logged_in_user():
    token = request.headers.get("Authorization")
    if not token:
        return None
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data
    except:
        return None
