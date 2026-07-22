from sqlalchemy import func
from app.models.product import Product
from app.models.order import Order
from app.models.rental import Rental
from app.models.review import Review
from app.models.user import User
from app.extensions import db


class AdminAIEngine:

    # ================= TOP SELLING PRODUCTS =================
    @staticmethod
    def top_selling_products(limit=5):

        return (
            db.session.query(
                Product.name,
                func.count(Order.id).label("sales")
            )
            .join(Order, Order.product_id == Product.id)
            .group_by(Product.id)
            .order_by(func.count(Order.id).desc())
            .limit(limit)
            .all()
        )


    # ================= MOST RENTED PRODUCTS =================
    @staticmethod
    def most_rented_products(limit=5):

        return (
            db.session.query(
                Product.name,
                func.count(Rental.id).label("rentals")
            )
            .join(Rental, Rental.product_id == Product.id)
            .group_by(Product.id)
            .order_by(func.count(Rental.id).desc())
            .limit(limit)
            .all()
        )


    # ================= HIGHEST RATED PRODUCTS =================
    @staticmethod
    def highest_rated_products(limit=5):

        return (
            db.session.query(
                Product.name,
                func.avg(Review.rating).label("rating")
            )
            .join(Review, Review.product_id == Product.id)
            .group_by(Product.id)
            .order_by(func.avg(Review.rating).desc())
            .limit(limit)
            .all()
        )


    # ================= MOST ACTIVE USERS =================
    @staticmethod
    def most_active_users(limit=5):

        return (
            db.session.query(
                User.name,
                func.count(Order.id).label("orders")
            )
            .join(Order, Order.user_id == User.id)
            .group_by(User.id)
            .order_by(func.count(Order.id).desc())
            .limit(limit)
            .all()
        )