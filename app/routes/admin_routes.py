from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.rental import Rental
from app.models.review import Review
from app.models.delivery_address import DeliveryAddress

from app.ai.admin_ai_engine import AdminAIEngine

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =========================================================
# ADMIN DASHBOARD
# =========================================================


@admin_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "admin":
        return "Unauthorized"

    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_rentals = Rental.query.count()
    total_reviews = Review.query.count()

    return render_template(
        "admin/dashboard.html",
        users=total_users,
        products=total_products,
        orders=total_orders,
        rentals=total_rentals,
        reviews=total_reviews
    )


# =========================================================
# USERS LIST
# =========================================================
@admin_bp.route("/users")
@login_required
def users():

    if current_user.role != "admin":
        return "Unauthorized"

    users = User.query.all()

    return render_template(
        "admin/users.html",
        users=users
    )


# =========================================================
# USER DETAIL
# =========================================================
@admin_bp.route("/user/<int:user_id>")
@login_required
def user_detail(user_id):

    if current_user.role != "admin":
        return "Unauthorized"

    user = User.query.get_or_404(user_id)

    return render_template(
        "admin/user_detail.html",
        user=user
    )


# =========================================================
# PRODUCTS LIST
# =========================================================
@admin_bp.route("/products")
@login_required
def products():

    if current_user.role != "admin":
        return "Unauthorized"

    products = Product.query.all()

    return render_template(
        "admin/products.html",
        products=products
    )


# =========================================================
# PRODUCT DETAIL
# =========================================================
@admin_bp.route("/product/<int:product_id>")
@login_required
def product_detail(product_id):

    if current_user.role != "admin":
        return "Unauthorized"

    product = Product.query.get_or_404(product_id)

    return render_template(
        "admin/product_detail.html",
        product=product
    )


# =========================================================
# ORDERS LIST
# =========================================================
@admin_bp.route("/orders")
@login_required
def orders():

    if current_user.role != "admin":
        return "Unauthorized"

    orders = Order.query.all()

    addresses = {
        a.order_id: a
        for a in DeliveryAddress.query.all()
    }

    return render_template(
        "admin/orders.html",
        orders=orders,
        addresses=addresses
    )


# =========================================================
# ORDER DETAIL
# =========================================================
@admin_bp.route("/order/<int:order_id>")
@login_required
def order_detail(order_id):

    if current_user.role != "admin":
        return "Unauthorized"

    order = Order.query.get_or_404(order_id)

    address = DeliveryAddress.query.filter_by(
        order_id=order.id
    ).first()

    return render_template(
        "admin/order_detail.html",
        order=order,
        address=address
    )


# =========================================================
# RENTALS LIST
# =========================================================
@admin_bp.route("/rentals")
@login_required
def rentals():

    if current_user.role != "admin":
        return "Unauthorized"

    rentals = Rental.query.all()

    return render_template(
        "admin/rentals.html",
        rentals=rentals
    )


# =========================================================
# RENTAL DETAIL
# =========================================================
@admin_bp.route("/rental/<int:rental_id>")
@login_required
def rental_detail(rental_id):

    if current_user.role != "admin":
        return "Unauthorized"

    rental = Rental.query.get_or_404(rental_id)

    return render_template(
        "admin/rental_detail.html",
        rental=rental
    )


# =========================================================
# 🤖 AI ANALYTICS DASHBOARD
# =========================================================
@admin_bp.route("/ai-dashboard")
@login_required
def ai_dashboard():

    if current_user.role != "admin":
        return "Unauthorized"

    top_products = AdminAIEngine.top_selling_products()
    rentals = AdminAIEngine.most_rented_products()
    ratings = AdminAIEngine.highest_rated_products()
    users = AdminAIEngine.most_active_users()

    return render_template(
        "admin/ai_dashboard.html",
        top_products=top_products,
        rentals=rentals,
        ratings=ratings,
        users=users
    )