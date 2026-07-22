from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user
from datetime import datetime

from app.extensions import db
from app.models.rental import Rental
from app.models.product import Product
from app.models.delivery_address import DeliveryAddress

rental_bp = Blueprint("rental", __name__, url_prefix="/rental")


# ================= RENTAL CHECKOUT =================
@rental_bp.route("/checkout/<int:product_id>", methods=["GET", "POST"])
@login_required
def rental_checkout(product_id):
    if current_user.role != "buyer":
        return "Unauthorized"

    product = Product.query.get_or_404(product_id)

    # ---------- SHOW RENTAL CHECKOUT PAGE ----------
    if request.method == "GET":
        return render_template(
            "rental/checkout.html",
            product=product
        )

    # ---------- PROCESS RENTAL ----------
    try:
        start_date = datetime.strptime(
            request.form["start_date"], "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            request.form["end_date"], "%Y-%m-%d"
        ).date()
    except Exception:
        return "Invalid date format"

    if end_date <= start_date:
        return "End date must be after start date"

    # ---------- AVAILABILITY CHECK ----------
    overlap = Rental.query.filter(
        Rental.product_id == product_id,
        Rental.rental_status == "ACTIVE",
        Rental.start_date <= end_date,
        Rental.end_date >= start_date
    ).first()

    if overlap:
        return "Product not available for selected dates"

    # ---------- RENT CALCULATION ----------
    days = (end_date - start_date).days
    total_rent = days * product.rental_price_per_day

    payment_method = request.form.get("payment_method")

    rental = Rental(
        user_id=current_user.id,
        product_id=product.id,
        start_date=start_date,
        end_date=end_date,
        total_rent=total_rent,
        deposit_paid=product.deposit_amount,
        payment_method=payment_method,
        payment_status="PAID" if payment_method != "COD" else "PENDING",
        rental_status="ACTIVE"
    )

    db.session.add(rental)
    db.session.flush()  # get rental.id

    # ---------- DELIVERY ADDRESS ----------
    address = DeliveryAddress(
        order_id=rental.id,
        full_name=request.form["full_name"],
        phone=request.form["phone"],
        address_line=request.form["address_line"],
        city=request.form["city"],
        state=request.form["state"],
        pincode=request.form["pincode"]
    )

    db.session.add(address)
    db.session.commit()

    return redirect("/buyer/rentals")


# ================= BUYER RENTALS =================
@rental_bp.route("/my-rentals")
@login_required
def my_rentals():
    if current_user.role != "buyer":
        return "Unauthorized"

    rentals = Rental.query.filter_by(user_id=current_user.id).all()
    products = {p.id: p for p in Product.query.all()}

    return render_template(
        "buyer/rentals.html",
        rentals=rentals,
        products=products
    )


# ================= RETURN RENTAL =================
@rental_bp.route("/return/<int:rental_id>")
@login_required
def return_product(rental_id):
    rental = Rental.query.get_or_404(rental_id)

    if rental.user_id != current_user.id:
        return "Unauthorized"

    rental.rental_status = "RETURNED"

    # OPTIONAL: refund deposit logic later
    rental.payment_status = "REFUNDED"

    db.session.commit()
    return redirect("/buyer/rentals")
