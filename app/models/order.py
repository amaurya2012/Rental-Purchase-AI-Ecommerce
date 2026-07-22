from app.extensions import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    # ---------------- RELATIONS ----------------
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    # ---------------- ORDER DETAILS ----------------
    quantity = db.Column(db.Integer, nullable=False)

    total_amount = db.Column(db.Float, nullable=False)

    # ---------------- PAYMENT DETAILS ----------------
    payment_method = db.Column(
        db.String(30),
        default="COD"        # COD | CARD | UPI
    )

    payment_status = db.Column(
        db.String(30),
        default="PENDING"    # PENDING | PAID
    )

    # ---------------- DELIVERY STATUS ----------------
    order_status = db.Column(
        db.String(30),
        default="PLACED"     # PLACED | SHIPPED | DELIVERED
    )

    # ---------------- TIMESTAMP ----------------
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Order {self.id} - User:{self.user_id} Product:{self.product_id}>"
