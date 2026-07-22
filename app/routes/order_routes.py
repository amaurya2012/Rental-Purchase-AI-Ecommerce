from flask import Blueprint, redirect, render_template, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.cart import Cart
from app.models.order import Order
from app.models.product import Product
from app.models.delivery_address import DeliveryAddress

order_bp = Blueprint("order", __name__, url_prefix="/order")


# ---------------- CHECKOUT PAGE (GET + POST) ----------------
@order_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    if current_user.role != "buyer":
        return "Unauthorized"

    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        return redirect("/buyer/dashboard")

    # ---------- SHOW CHECKOUT PAGE ----------
    if request.method == "GET":
        return render_template("order/checkout.html")

    # ---------- PLACE ORDER ----------
    payment_method = request.form.get("payment_method")

    for item in cart_items:
        product = Product.query.get_or_404(item.product_id)

        if product.quantity_available < item.quantity:
            return f"Insufficient stock for {product.name}"

        # Reduce stock
        product.quantity_available -= item.quantity

        # Create order
        order = Order(
            user_id=current_user.id,
            product_id=product.id,
            quantity=item.quantity,
            total_amount=product.purchase_price * item.quantity,
            payment_method=payment_method,
            payment_status="PAID" if payment_method != "COD" else "PENDING"
        )

        db.session.add(order)
        db.session.flush()  # get order.id before commit

        # Save delivery address
        address = DeliveryAddress(
            order_id=order.id,
            full_name=request.form.get("full_name"),
            phone=request.form.get("phone"),
            address_line=request.form.get("address_line"),
            city=request.form.get("city"),
            state=request.form.get("state"),
            pincode=request.form.get("pincode")
        )

        db.session.add(address)

    # Clear cart after successful order
    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return redirect("/buyer/orders")


# ---------------- MY ORDERS ----------------
@order_bp.route("/my-orders")
@login_required
def my_orders():
    if current_user.role != "buyer":
        return "Unauthorized"

    orders = Order.query.filter_by(user_id=current_user.id).all()
    products = {p.id: p for p in Product.query.all()}

    return render_template(
        "buyer/orders.html",
        orders=orders,
        products=products
    )
