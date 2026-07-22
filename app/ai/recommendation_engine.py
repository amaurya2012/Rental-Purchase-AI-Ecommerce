from sqlalchemy import func
from app.models.interaction import Interaction
from app.models.product import Product
from app.extensions import db


class RecommendationEngine:

    @staticmethod
    def get_user_recommendations(user_id, limit=6):
        """
        Recommend products based on user behavior
        """

        ranked_products = (
            db.session.query(
                Interaction.product_id,
                func.count(Interaction.id).label("score")
            )
            .filter(Interaction.user_id == user_id)
            .group_by(Interaction.product_id)
            .order_by(func.count(Interaction.id).desc())
            .limit(limit)
            .all()
        )

        product_ids = [p.product_id for p in ranked_products]

        if not product_ids:
            return Product.query.order_by(Product.created_at.desc()).limit(limit).all()

        return Product.query.filter(Product.id.in_(product_ids)).all()