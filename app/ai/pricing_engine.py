from datetime import datetime, timedelta
from app.models.rental import Rental


class PricingEngine:

    @staticmethod
    def get_dynamic_price(product):

        base_price = product.rental_price_per_day

        last_week = datetime.utcnow() - timedelta(days=7)

        demand = Rental.query.filter(
            Rental.product_id == product.id,
            Rental.created_at >= last_week
        ).count()

        if demand > 10:
            return round(base_price * 1.35, 2)

        elif demand > 5:
            return round(base_price * 1.20, 2)

        elif demand > 2:
            return round(base_price * 1.10, 2)

        return base_price