from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.rental import Rental

from app.ai.recommendation_engine import RecommendationEngine
from app.ai.wishlist_engine import WishlistEngine


buyer_bp = Blueprint("buyer", __name__, url_prefix="/buyer")


# =========================================================
# BUYER DASHBOARD
# =========================================================
@buyer_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "buyer":
        return "Unauthorized Access"

    # Filters
    category_id = request.args.get("category")
    search = request.args.get("search")
    sort = request.args.get("sort")

    categories = Category.query.all()

    query = Product.query

    # Category Filter
    if category_id:
        try:
            category_id = int(category_id)
            query = query.filter(Product.category_id == category_id)
        except:
            pass

    # Search Filter
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # Price Sorting
    if sort == "low":
        query = query.order_by(Product.purchase_price.asc())

    elif sort == "high":
        query = query.order_by(Product.purchase_price.desc())

    products = query.all()

    # ================= AI FEATURES =================
    recommended_products = RecommendationEngine.get_user_recommendations(
        current_user.id
    )

    wishlist_recommendations = WishlistEngine.get_similar_products(
        current_user.id
    )

    return render_template(
        "buyer/dashboard.html",
        products=products,
        categories=categories,
        selected_category=category_id,
        search=search,
        sort=sort,
        recommended=recommended_products,
        wishlist_recommend=wishlist_recommendations
    )


# =========================================================
# BUYER ORDERS
# =========================================================
@buyer_bp.route("/orders")
@login_required
def buyer_orders():

    if current_user.role != "buyer":
        return "Unauthorized Access"

    orders = Order.query.filter_by(
        user_id=current_user.id
    ).all()

    # Map products for display
    products = {p.id: p for p in Product.query.all()}

    return render_template(
        "buyer/orders.html",
        orders=orders,
        products=products
    )


# =========================================================
# BUYER RENTALS
# =========================================================
@buyer_bp.route("/rentals")
@login_required
def buyer_rentals():

    if current_user.role != "buyer":
        return "Unauthorized Access"

    rentals = Rental.query.filter_by(
        user_id=current_user.id
    ).all()

    # Map products for display
    products = {p.id: p for p in Product.query.all()}

    return render_template(
        "buyer/rentals.html",
        rentals=rentals,
        products=products
    )