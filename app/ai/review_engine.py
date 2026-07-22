from sqlalchemy import func
from app.models.review import Review
from app.extensions import db


class ReviewEngine:

    @staticmethod
    def get_average_rating(product_id):

        rating = (
            db.session.query(func.avg(Review.rating))
            .filter(Review.product_id == product_id)
            .scalar()
        )

        return round(rating or 0, 2)


    @staticmethod
    def get_total_reviews(product_id):

        return Review.query.filter_by(product_id=product_id).count()