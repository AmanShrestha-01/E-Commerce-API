from flask import Flask, jsonify
from models import db
from products.routes import products_bp
from auth.routes import auth_bp, bcrypt
from cart.routes import cart_bp
from orders.routes import orders_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(products_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(orders_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "E-Commerce API is running"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
