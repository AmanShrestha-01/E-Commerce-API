from flask import Blueprint, jsonify, request
from models import db, Product

products_bp = Blueprint("products", __name__)


def product_to_dict(p):
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "stock": p.stock,
        "category": p.category
    }


@products_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    result = []
    for p in products:
        result.append(product_to_dict(p))
    return jsonify(result)


@products_bp.route("/products", methods=["POST"])
def add_product():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if "name" not in data or "price" not in data or "stock" not in data or "category" not in data:
        return jsonify({"error": "name, price, stock, and category are required"}), 400
    product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=data["price"],
        stock=data["stock"],
        category=data["category"]
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product_to_dict(product)), 201
