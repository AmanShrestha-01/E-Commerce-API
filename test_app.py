import json
from app import app, db

def get_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    with app.app_context():
        db.create_all()
    return app.test_client()

def get_token(client):
    client.post("/signup",
        data=json.dumps({"username": "testuser", "password": "testpass123"}),
        content_type="application/json"
    )
    response = client.post("/login",
        data=json.dumps({"username": "testuser", "password": "testpass123"}),
        content_type="application/json"
    )
    data = json.loads(response.data)
    return data["token"]

def test_home():
    client = get_client()
    response = client.get("/")
    assert response.status_code == 200
    print("PASS: Home route works")

def test_signup():
    client = get_client()
    response = client.post("/signup",
        data=json.dumps({"username": "newuser", "password": "pass123"}),
        content_type="application/json"
    )
    assert response.status_code == 201
    print("PASS: Signup works")

def test_signup_duplicate():
    client = get_client()
    client.post("/signup",
        data=json.dumps({"username": "dupeuser", "password": "pass123"}),
        content_type="application/json"
    )
    response = client.post("/signup",
        data=json.dumps({"username": "dupeuser", "password": "pass123"}),
        content_type="application/json"
    )
    assert response.status_code == 409
    print("PASS: Duplicate signup rejected")

def test_login():
    client = get_client()
    client.post("/signup",
        data=json.dumps({"username": "loginuser", "password": "pass123"}),
        content_type="application/json"
    )
    response = client.post("/login",
        data=json.dumps({"username": "loginuser", "password": "pass123"}),
        content_type="application/json"
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "token" in data
    print("PASS: Login works and returns token")

def test_create_product():
    client = get_client()
    response = client.post("/products",
        data=json.dumps({"name": "Test Product", "price": 29.99, "stock": 10, "category": "test"}),
        content_type="application/json"
    )
    assert response.status_code == 201
    print("PASS: Product creation works")

def test_cart_requires_login():
    client = get_client()
    response = client.get("/cart")
    assert response.status_code == 401
    print("PASS: Cart rejects unauthenticated users")

if __name__ == "__main__":
    test_home()
    test_signup()
    test_signup_duplicate()
    test_login()
    test_create_product()
    test_cart_requires_login()
    print("\nAll tests passed!")
