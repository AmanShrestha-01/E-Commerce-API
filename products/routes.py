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
    """
    Get all products
    ---
    tags:
      - Products
    responses:
      200:
        description: A list of all products
    """
    products = Product.query.all()
    result = []
    for p in products:
        result.append(product_to_dict(p))
    return jsonify(result)


@products_bp.route("/products", methods=["POST"])
def add_product():
    """
    Create a new product
    ---
    tags:
      - Products
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: iPhone
            price:
              type: number
              example: 999.99
            stock:
              type: integer
              example: 50
            category:
              type: string
              example: electronics
            description:
              type: string
              example: Latest smartphone
    responses:
      201:
        description: Product created
      400:
        description: Invalid input
    """
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
