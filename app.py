from flask import Flask, render_template, send_from_directory, redirect, url_for
from flask_login import LoginManager, current_user, login_required

from models import db
from models.user import User
from models.product import Product

from routes.auth import auth
from routes.products import products
from routes.orders import orders
from routes.dashboard import dashboard
from config import Config

import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


# ==========================================
# APPLICATION SETTINGS
# ==========================================

app.config.from_object(Config)


# ==========================================
# INITIALIZE DATABASE
# ==========================================

db.init_app(app)


# ==========================================
# INITIALIZE LOGIN MANAGER
# ==========================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


# ==========================================
# REGISTER BLUEPRINTS
# ==========================================

app.register_blueprint(auth)

app.register_blueprint(products)

app.register_blueprint(orders)

app.register_blueprint(dashboard)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def index():

    # If already logged in, go to Seller / Buyer page

    # If not logged in, show BorrowBay home page
    return render_template("index.html")


# ==========================================
# SELLER / BUYER SELECTION PAGE
# ==========================================

@app.route("/choose-role")
@login_required
def choose_role():

    return render_template(
        "choose_role.html"
    )


# ==========================================
# PRODUCT IMAGE ROUTE
# ==========================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# ==========================================
# CREATE FOLDERS AND DATABASE
# ==========================================

with app.app_context():

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    os.makedirs(
        os.path.join(
            BASE_DIR,
            "database"
        ),
        exist_ok=True
    )

    db.create_all()


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)