from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login_manager
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- LOGIN ----------------
@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email, is_active=True).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            # ROLE BASED REDIRECT
            if user.role == "admin":
                return redirect("/admin/dashboard")
            elif user.role == "seller":
                return redirect("/seller/dashboard")
            else:
                return redirect("/buyer/dashboard")

        flash("Invalid email or password", "danger")

    return render_template("auth/login.html")


# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "warning")
            return redirect("/register")

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect("/login")

    return render_template("auth/register.html")


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect("/login")
