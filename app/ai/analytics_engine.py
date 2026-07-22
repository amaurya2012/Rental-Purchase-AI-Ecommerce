from sqlalchemy import func
from app.models.product import Product
from app.models.order import Order
from app.models.rental import Rental
from app.models.user import User
from app.extensions import db


class AnalyticsEngine:

    @staticmethod
    def top_selling_products(limit=5):

        return (
            db.session.query(Product.name, func.count(Order.id))
            .join(Order)
            .group_by(Product.id)
            .order_by(func.count(Order.id).desc())
            .limit(limit)
            .all()
        )


    @staticmethod
    def most_rented_products(limit=5):

        return (
            db.session.query(Product.name, func.count(Rental.id))
            .join(Rental)
            .group_by(Product.id)
            .order_by(func.count(Rental.id).desc())
            .limit(limit)
            .all()
        )


    @staticmethod
    def most_active_users(limit=5):

        return (
            db.session.query(User.name, func.count(Order.id))
            .join(Order)
            .group_by(User.id)
            .order_by(func.count(Order.id).desc())
            .limit(limit)
            .all()
        )