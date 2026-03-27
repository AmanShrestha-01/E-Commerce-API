from flask import Blueprint, jsonify, request
from models import db, CartItem, Product
from middleware import get_logged_in_user

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart", methods=["GET"])
def get_cart():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    items = CartItem.query.filter_by(user_id=user["user_id"]).all()
    result = []
    for item in items:
        product = Product.query.get(item.product_id)
        result.append({
            "id": item.id,
            "product_name": product.name,
            "product_price": product.price,
            "quantity": item.quantity,
            "subtotal": product.price * item.quantity
        })
    return jsonify(result)

@cart_bp.route("/cart", methods=["POST"])
def add_to_cart():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if "product_id" not in data:
        return jsonify({"error": "product_id is required"}), 400
    product = Product.query.get(data["product_id"])
    if not product:
        return jsonify({"error": "Product not found"}), 404
    if product.stock < data.get("quantity", 1):
        return jsonify({"error": "Not enough stock"}), 400
    existing = CartItem.query.filter_by(
        user_id=user["user_id"],
        product_id=data["product_id"]
    ).first()
    if existing:
        existing.quantity += data.get("quantity", 1)
    else:
        item = CartItem(
            user_id=user["user_id"],
            product_id=data["product_id"],
            quantity=data.get("quantity", 1)
        )
        db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Added to cart"}), 201

@cart_bp.route("/cart/<int:item_id>", methods=["DELETE"])
def remove_from_cart(item_id):
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    item = CartItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    if item.user_id != user["user_id"]:
        return jsonify({"error": "This is not your cart item"}), 403
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Removed from cart"})
