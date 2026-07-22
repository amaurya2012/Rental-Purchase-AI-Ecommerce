from app.models.wishlist import Wishlist
from app.models.product import Product


class WishlistEngine:

    @staticmethod
    def get_similar_products(user_id, limit=5):

        items = Wishlist.query.filter_by(user_id=user_id).all()

        if not items:
            return []

        categories = []

        for item in items:
            product = Product.query.get(item.product_id)
            if product:
                categories.append(product.category_id)

        return Product.query.filter(
            Product.category_id.in_(categories)
        ).limit(limit).all()