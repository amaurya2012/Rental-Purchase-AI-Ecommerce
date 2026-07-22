from flask import Blueprint, redirect, render_template
from flask_login import login_required, current_user

from app.extensions import db
from app.models.cart import Cart
from app.models.product import Product

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


# ---------------- ADD TO CART ----------------
@cart_bp.route("/add/<int:product_id>")
@login_required
def add_to_cart(product_id):
    if current_user.role != "buyer":
        return "Unauthorized"

    item = Cart.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if item:
        item.quantity += 1
    else:
        item = Cart(
            user_id=current_user.id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(item)

    db.session.commit()
    return redirect("/cart/view")


# ---------------- INCREASE QUANTITY ----------------
@cart_bp.route("/increase/<int:item_id>")
@login_required
def increase_quantity(item_id):
    item = Cart.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        return "Unauthorized"

    item.quantity += 1
    db.session.commit()
    return redirect("/cart/view")


# ---------------- DECREASE QUANTITY ----------------
@cart_bp.route("/decrease/<int:item_id>")
@login_required
def decrease_quantity(item_id):
    item = Cart.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        return "Unauthorized"

    if item.quantity > 1:
        item.quantity -= 1
    else:
        db.session.delete(item)

    db.session.commit()
    return redirect("/cart/view")


# ---------------- VIEW CART ----------------
@cart_bp.route("/view")
@login_required
def view_cart():
    if current_user.role != "buyer":
        return "Unauthorized"

    items = Cart.query.filter_by(user_id=current_user.id).all()

    products = []
    total = 0

    for item in items:
        product = Product.query.get(item.product_id)
        subtotal = product.purchase_price * item.quantity
        total += subtotal

        products.append({
            "item_id": item.id,
            "product": product,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return render_template(
        "buyer/cart.html",
        products=products,
        total=total
    )


# ---------------- REMOVE ITEM ----------------
@cart_bp.route("/remove/<int:item_id>")
@login_required
def remove_item(item_id):
    Cart.query.filter_by(
        id=item_id,
        user_id=current_user.id
    ).delete()

    db.session.commit()
    return redirect("/cart/view")
