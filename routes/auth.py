from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from models import db
from models.user import User


auth = Blueprint("auth", __name__)


# ==========================================
# REGISTER
# ==========================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash("Email already registered.")

            return redirect(
                url_for("auth.register")
            )

        user = User(
            name=name,
            email=email
        )

        user.set_password(password)

        db.session.add(user)

        db.session.commit()

        flash(
            "Registration successful. Please login."
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


# ==========================================
# LOGIN
# ==========================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.check_password(password):

            login_user(
                user,
                remember=True
            )

            # After successful login,
            # show Seller / Buyer page
            return redirect(
                url_for("choose_role")
            )

        flash(
            "Invalid email or password."
        )

    # Always show login page
    return render_template(
        "login.html"
    )


# ==========================================
# LOGOUT
# ==========================================

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out."
    )

    return redirect(
        url_for("index")
    )