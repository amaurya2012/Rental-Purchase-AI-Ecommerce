from flask import Blueprint, redirect, render_template
from flask_login import login_required, current_user

from app.extensions import db
from app.models.wishlist import Wishlist
from app.models.product import Product

wishlist_bp = Blueprint("wishlist", __name__, url_prefix="/wishlist")


# ================= ADD TO WISHLIST =================
@wishlist_bp.route("/add/<int:product_id>")
@login_required
def add(product_id):

    existing = Wishlist.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if not existing:
        db.session.add(
            Wishlist(
                user_id=current_user.id,
                product_id=product_id
            )
        )
        db.session.commit()

    return redirect("/wishlist/view")


# ================= VIEW WISHLIST =================
@wishlist_bp.route("/view")
@login_required
def view():

    items = Wishlist.query.filter_by(
        user_id=current_user.id
    ).all()

    products = {p.id: p for p in Product.query.all()}

    return render_template(
        "buyer/wishlist.html",
        items=items,
        products=products
    )


# ================= REMOVE FROM WISHLIST =================
@wishlist_bp.route("/remove/<int:item_id>")
@login_required
def remove(item_id):

    item = Wishlist.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        return "Unauthorized"

    db.session.delete(item)
    db.session.commit()

    return redirect("/wishlist/view")