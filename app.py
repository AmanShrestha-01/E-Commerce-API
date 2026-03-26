from flask import Flask,jsonify
from models import db
from products.routes import products_bp
from auth.routes import auth_bp, bcrypt

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///ecommerce.db"

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(products_bp)
app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "E-Commerce API is running"})


app.run(debug=True, port=8000)