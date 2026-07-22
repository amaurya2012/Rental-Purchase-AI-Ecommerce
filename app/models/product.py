from app.extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

    purchase_price = db.Column(db.Float, nullable=False)
    rental_price_per_day = db.Column(db.Float, nullable=True)

    deposit_amount = db.Column(db.Float, default=0.0)
    quantity_available = db.Column(db.Integer, default=1)

    image_filename = db.Column(db.String(200))

    seller_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # ✅ REQUIRED FOR CATEGORY MANAGEMENT & FILTERING
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Product {self.name}>"
