from flask import Blueprint, jsonify, request
from models import db, Order, OrderItem, CartItem, Product
from middleware import get_logged_in_user
import datetime

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/orders", methods=["POST"])
def place_order():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    cart_items = CartItem.query.filter_by(user_id=user["user_id"]).all()
    if len(cart_items) == 0:
        return jsonify({"error": "Your cart is empty"}), 400
    total_price = 0
    order_items_data = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if not product:
            return jsonify({"error": f"Product {item.product_id} not found"}), 404
        if product.stock < item.quantity:
            return jsonify({"error": f"Not enough stock for {product.name}"}), 400
        subtotal = product.price * item.quantity
        total_price += subtotal
        order_items_data.append({
            "product_id": product.id,
            "quantity": item.quantity,
            "price": product.price
        })
    order = Order(
        user_id=user["user_id"],
        total_price=total_price,
        created_at=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.session.add(order)
    db.session.commit()
    for data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=data["product_id"],
            quantity=data["quantity"],
            price=data["price"]
        )
        db.session.add(order_item)
    for item in cart_items:
        product = Product.query.get(item.product_id)
        product.stock -= item.quantity
        db.session.delete(item)
    db.session.commit()
    return jsonify({
        "message": "Order placed",
        "order_id": order.id,
        "total_price": order.total_price,
        "status": order.status
    }), 201

@orders_bp.route("/orders", methods=["GET"])
def get_orders():
    user = get_logged_in_user()
    if not user:
        return jsonify({"error": "You must be logged in"}), 401
    orders = Order.query.filter_by(user_id=user["user_id"]).all()
    result = []
    for order in orders:
        items = OrderItem.query.filter_by(order_id=order.id).all()
        order_items = []
        for item in items:
            product = Product.query.get(item.product_id)
            order_items.append({
                "product_name": product.name,
                "quantity": item.quantity,
                "price": item.price,
                "subtotal": item.price * item.quantity
            })
        result.append({
            "id": order.id,
            "total_price": order.total_price,
            "status": order.status,
            "created_at": order.created_at,
            "items": order_items
        })
    return jsonify(result)
