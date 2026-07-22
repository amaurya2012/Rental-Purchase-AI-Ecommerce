import os
from flask import Blueprint, render_template, request, redirect, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.review import Review

product_bp = Blueprint("product", __name__, url_prefix="/product")


# =====================================================
# ADD PRODUCT (SELLER)
# =====================================================
@product_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_product():

    if current_user.role != "seller":
        abort(403)

    categories = Category.query.all()

    if request.method == "POST":

        name = request.form.get("name")
        description = request.form.get("description")

        purchase_price = float(request.form.get("purchase_price").replace(",", ""))
        rental_price = float(request.form.get("rental_price").replace(",", ""))
        deposit = float(request.form.get("deposit").replace(",", ""))
        quantity = int(request.form.get("quantity"))
        category_id = int(request.form.get("category_id"))

        image = request.files.get("image")
        filename = None

        if image and image.filename:
            filename = secure_filename(image.filename)
            upload_path = current_app.config["UPLOAD_FOLDER"]

            os.makedirs(upload_path, exist_ok=True)

            image.save(os.path.join(upload_path, filename))

        product = Product(
            name=name,
            description=description,
            purchase_price=purchase_price,
            rental_price_per_day=rental_price,
            deposit_amount=deposit,
            quantity_available=quantity,
            image_filename=filename,
            seller_id=current_user.id,
            category_id=category_id
        )

        db.session.add(product)
        db.session.commit()

        return redirect("/product/my-products")

    return render_template(
        "seller/add_product.html",
        categories=categories
    )


# =====================================================
# MY PRODUCTS (SELLER)
# =====================================================
@product_bp.route("/my-products")
@login_required
def my_products():

    if current_user.role != "seller":
        abort(403)

    products = Product.query.filter_by(
        seller_id=current_user.id
    ).all()

    categories = Category.query.all()

    category_map = {c.id: c for c in categories}

    return render_template(
        "seller/my_products.html",
        products=products,
        category_map=category_map
    )


# =====================================================
# EDIT PRODUCT (SELLER)
# =====================================================
@product_bp.route("/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):

    product = Product.query.get_or_404(product_id)

    if current_user.role != "seller" or product.seller_id != current_user.id:
        abort(403)

    categories = Category.query.all()

    if request.method == "POST":

        product.name = request.form.get("name")
        product.description = request.form.get("description")

        product.purchase_price = float(
            request.form.get("purchase_price").replace(",", "")
        )

        product.rental_price_per_day = float(
            request.form.get("rental_price").replace(",", "")
        )

        product.deposit_amount = float(
            request.form.get("deposit").replace(",", "")
        )

        product.quantity_available = int(request.form.get("quantity"))
        product.category_id = int(request.form.get("category_id"))

        image = request.files.get("image")

        if image and image.filename:
            filename = secure_filename(image.filename)

            upload_path = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_path, exist_ok=True)

            image.save(os.path.join(upload_path, filename))

            product.image_filename = filename

        db.session.commit()

        return redirect("/product/my-products")

    return render_template(
        "seller/edit_product.html",
        product=product,
        categories=categories
    )


# =====================================================
# DELETE PRODUCT (SELLER)
# =====================================================
@product_bp.route("/delete/<int:product_id>")
@login_required
def delete_product(product_id):

    product = Product.query.get_or_404(product_id)

    if current_user.role != "seller" or product.seller_id != current_user.id:
        abort(403)

    db.session.delete(product)
    db.session.commit()

    return redirect("/product/my-products")


# =====================================================
# PRODUCT DETAIL (BUYER)
# =====================================================
@product_bp.route("/<int:product_id>")
@login_required
def product_detail(product_id):

    product = Product.query.get_or_404(product_id)

    reviews = Review.query.filter_by(
        product_id=product_id
    ).all()

    return render_template(
        "product/product_detail.html",
        product=product,
        reviews=reviews
    )


# =====================================================
# ADD REVIEW (BUYER)
# =====================================================
@product_bp.route("/review/add/<int:product_id>", methods=["POST"])
@login_required
def add_review(product_id):

    rating = int(request.form.get("rating"))
    comment = request.form.get("comment")

    review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )

    db.session.add(review)
    db.session.commit()

    return redirect(f"/product/{product_id}")