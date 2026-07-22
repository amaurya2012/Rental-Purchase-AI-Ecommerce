from flask import Flask
from flask_login import current_user

from .config import Config
from .extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ---------------- INITIALIZE EXTENSIONS ----------------
    db.init_app(app)
    login_manager.init_app(app)

    # ---------------- IMPORT MODELS ----------------
    # IMPORTANT: Models must be imported BEFORE create_all()
    from .models.user import User
    from .models.product import Product
    from .models.cart import Cart
    from .models.order import Order
    from .models.rental import Rental
    from .models.interaction import Interaction
    from .models.delivery_address import DeliveryAddress

    # ---------------- REGISTER BLUEPRINTS ----------------
    from .routes.auth_routes import auth_bp
    from .routes.buyer_routes import buyer_bp
    from .routes.seller_routes import seller_bp
    from .routes.admin_routes import admin_bp
    from .routes.product_routes import product_bp
    from .routes.cart_routes import cart_bp
    from .routes.order_routes import order_bp
    from .routes.rental_routes import rental_bp
    from .routes.review_routes import review_bp
    from .routes.wishlist_routes import wishlist_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(buyer_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(rental_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(wishlist_bp)
    # ---------------- GLOBAL CART COUNT (ALL TEMPLATES) ----------------
    @app.context_processor
    def inject_cart_count():
        if current_user.is_authenticated and getattr(current_user, "role", None) == "buyer":
            count = Cart.query.filter_by(user_id=current_user.id).count()
        else:
            count = 0
        return dict(cart_count=count)

    # ---------------- CREATE DATABASE TABLES ----------------
    with app.app_context():
        db.create_all()

    return app
