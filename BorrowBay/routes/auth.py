
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import login_user, logout_user, login_required

from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from models import db
from models.user import User

from extensions import mail


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

        flash("Registration successful. Please login.")

        return redirect(
            url_for("auth.login")
        )

    return render_template("register.html")


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

            return redirect(
                url_for("choose_role")
            )

        flash("Invalid email or password.")

    return render_template("login.html")


# ==========================================
# LOGOUT
# ==========================================

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.")

    return redirect(
        url_for("index")
    )


# ==========================================
# FORGOT PASSWORD
# ==========================================

@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        user = User.query.filter_by(
            email=email
        ).first()

        if user:

            serializer = URLSafeTimedSerializer(
                current_app.config["SECRET_KEY"]
            )

            token = serializer.dumps(
                user.email,
                salt="password-reset"
            )

            reset_link = current_app.config["PUBLIC_BASE_URL"].rstrip("/") + url_for(
    "auth.reset_password",
    token=token
)

            msg = Message(
                "BorrowBay - Password Reset",
                recipients=[user.email]
            )

            msg.body = f"""
Hello {user.name},

We received a request to reset your BorrowBay password.

Click the link below to create a new password:

{reset_link}

This link will expire in 30 minutes.

If you did not request a password reset, you can ignore this email.

Regards,
BorrowBay
"""

            mail.send(msg)

        flash(
            "If an account with that email exists, "
            "a password reset link has been sent."
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template("forgot_password.html")


# ==========================================
# RESET PASSWORD
# ==========================================

@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:

        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=1800
        )

    except SignatureExpired:

        flash("The password reset link has expired.")
        return redirect(
            url_for("auth.forgot_password")
        )

    except BadSignature:

        flash("The password reset link is invalid.")
        return redirect(
            url_for("auth.forgot_password")
        )

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:

        flash("Invalid password reset request.")
        return redirect(
            url_for("auth.forgot_password")
        )

    if request.method == "POST":

        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            flash("Passwords do not match.")
            return render_template(
                "reset_password.html"
            )

        if not password:

            flash("Password cannot be empty.")
            return render_template(
                "reset_password.html"
            )

        user.set_password(password)

        db.session.commit()

        flash(
            "Password reset successful. "
            "Please login with your new password."
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "reset_password.html"
    )