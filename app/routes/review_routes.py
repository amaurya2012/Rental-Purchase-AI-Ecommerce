from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from app.extensions import db
from app.models.review import Review

review_bp = Blueprint("review", __name__, url_prefix="/review")


@review_bp.route("/add/<int:product_id>", methods=["POST"])
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