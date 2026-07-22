from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
import os

from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.rental import Rental
from app.models.delivery_address import DeliveryAddress

seller_bp = Blueprint("seller", __name__, url_prefix="/seller")


# ================= DASHBOARD =================
@seller_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "seller":
        return "Unauthorized"

    products = Product.query.filter_by(seller_id=current_user.id).all()
    product_ids = [p.id for p in products]

    orders = Order.query.filter(Order.product_id.in_(product_ids)).all()
    rentals = Rental.query.filter(Rental.product_id.in_(product_ids)).all()

    products_map = {p.id: p for p in products}
    addresses = {a.order_id: a for a in DeliveryAddress.query.all()}

    return render_template(
        "seller/dashboard.html",
        products=products,
        orders=orders,
        rentals=rentals,
        products_map=products_map,
        addresses=addresses
    )


# ================= CATEGORY MANAGEMENT =================
@seller_bp.route("/categories")
@login_required
def categories():
    categories = Category.query.filter_by(seller_id=current_user.id).all()
    return render_template("seller/categories.html", categories=categories)


@seller_bp.route("/category/add", methods=["GET", "POST"])
@login_required
def add_category():
    if request.method == "POST":
        db.session.add(Category(
            name=request.form["name"],
            seller_id=current_user.id
        ))
        db.session.commit()
        return redirect("/seller/categories")

    return render_template("seller/add_category.html")


@seller_bp.route("/category/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    if category.seller_id != current_user.id:
        return "Unauthorized"

    if request.method == "POST":
        category.name = request.form["name"]
        db.session.commit()
        return redirect("/seller/categories")

    return render_template("seller/edit_category.html", category=category)


@seller_bp.route("/category/delete/<int:id>")
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    if category.seller_id != current_user.id:
        return "Unauthorized"

    if Product.query.filter_by(category_id=id).first():
        return "Cannot delete category with products"

    db.session.delete(category)
    db.session.commit()
    return redirect("/seller/categories")


# ================= PRODUCT MANAGEMENT =================
@seller_bp.route("/my-products")
@login_required
def my_products():
    products = Product.query.filter_by(seller_id=current_user.id).all()
    categories = {c.id: c for c in Category.query.filter_by(seller_id=current_user.id)}
    return render_template(
        "seller/my_products.html",
        products=products,
        categories=categories
    )


@seller_bp.route("/product/add", methods=["GET", "POST"])
@login_required
def add_product():
    categories = Category.query.filter_by(seller_id=current_user.id).all()

    if request.method == "POST":
        image = request.files["image"]
        filename = image.filename
        upload_path = "app/static/uploads"
        os.makedirs(upload_path, exist_ok=True)
        image.save(os.path.join(upload_path, filename))

        product = Product(
            name=request.form["name"],
            description=request.form["description"],
            purchase_price=float(request.form["purchase_price"]),
            rental_price_per_day=float(request.form["rental_price"]),
            deposit_amount=float(request.form["deposit"]),
            quantity_available=int(request.form["quantity"]),
            image_filename=filename,
            seller_id=current_user.id,
            category_id=int(request.form["category_id"])
        )

        db.session.add(product)
        db.session.commit()
        return redirect("/seller/my-products")

    return render_template("seller/add_product.html", categories=categories)


@seller_bp.route("/product/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if product.seller_id != current_user.id:
        return "Unauthorized"

    categories = Category.query.filter_by(seller_id=current_user.id).all()

    if request.method == "POST":
        product.name = request.form["name"]
        product.description = request.form["description"]
        product.purchase_price = float(request.form["purchase_price"])
        product.rental_price_per_day = float(request.form["rental_price"])
        product.deposit_amount = float(request.form["deposit"])
        product.quantity_available = int(request.form["quantity"])
        product.category_id = int(request.form["category_id"])

        image = request.files.get("image")
        if image and image.filename:
            image.save(f"app/static/uploads/{image.filename}")
            product.image_filename = image.filename

        db.session.commit()
        return redirect("/seller/my-products")

    return render_template(
        "seller/edit_product.html",
        product=product,
        categories=categories
    )


@seller_bp.route("/product/delete/<int:id>")
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    if product.seller_id != current_user.id:
        return "Unauthorized"

    db.session.delete(product)
    db.session.commit()
    return redirect("/seller/my-products")
# ================= UPDATE ORDER STATUS =================
@seller_bp.route("/order/update/<int:order_id>", methods=["POST"])
@login_required
def update_order(order_id):
    if current_user.role != "seller":
        return "Unauthorized"

    order = Order.query.get_or_404(order_id)

    # Ensure seller owns the product
    product = Product.query.get(order.product_id)
    if product.seller_id != current_user.id:
        return "Unauthorized"

    order.order_status = request.form.get("status")
    db.session.commit()

    return redirect("/seller/dashboard")
