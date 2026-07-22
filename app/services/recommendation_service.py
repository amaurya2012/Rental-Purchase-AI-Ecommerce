from sqlalchemy import func
from app.models.interaction import Interaction
from app.models.product import Product

def get_recommended_products(user_id):

    interactions = (
        Interaction.query
        .filter_by(user_id=user_id)
        .with_entities(
            Interaction.product_id,
            func.count().label("score")
        )
        .group_by(Interaction.product_id)
        .order_by(func.count().desc())
        .limit(6)
        .all()
    )

    ids = [i.product_id for i in interactions]

    return Product.query.filter(Product.id.in_(ids)).all()