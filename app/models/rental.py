from app.extensions import db
from datetime import datetime


class Rental(db.Model):
    __tablename__ = "rentals"

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

    # ---------------- RENTAL PERIOD ----------------
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # ---------------- PRICING ----------------
    total_rent = db.Column(db.Float, nullable=False)
    deposit_paid = db.Column(db.Float, nullable=False)

    # ---------------- PAYMENT DETAILS ----------------
    payment_method = db.Column(
        db.String(30),
        default="COD"          # COD | CARD | UPI
    )

    payment_status = db.Column(
        db.String(30),
        default="PENDING"      # PENDING | PAID | REFUNDED
    )

    # ---------------- RENTAL STATUS ----------------
    rental_status = db.Column(
        db.String(30),
        default="ACTIVE"       # ACTIVE | RETURNED | LATE
    )

    # ---------------- TIMESTAMP ----------------
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Rental {self.id} User:{self.user_id} Product:{self.product_id}>"
