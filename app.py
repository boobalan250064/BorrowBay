from flask import Flask, render_template, send_from_directory
from flask_login import LoginManager, login_required

from models import db
from models.user import User
from models.product import Product
from models.order import Order
from models.cart import Cart
from models.verification import PurchaseVerification

from routes.auth import auth
from routes.products import products
from routes.orders import orders
from routes.dashboard import dashboard

from config import Config

import os


# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


# ==========================================
# CREATE FLASK APPLICATION
# ==========================================

app = Flask(__name__)


# ==========================================
# APPLICATION SETTINGS
# ==========================================

app.config.from_object(Config)


# Upload folder
app.config["UPLOAD_FOLDER"] = os.path.join(
    BASE_DIR,
    "uploads"
)


# Maximum upload size = 5 MB
app.config["MAX_CONTENT_LENGTH"] = (
    5 * 1024 * 1024
)


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


# ==========================================
# LOAD LOGGED-IN USER
# ==========================================

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

    return render_template(
        "index.html"
    )


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
# CREATE REQUIRED FOLDERS
# ==========================================

with app.app_context():

    # Create uploads folder
    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    # Create database folder
    os.makedirs(
        os.path.join(
            BASE_DIR,
            "database"
        ),
        exist_ok=True
    )

    # Create database tables
    db.create_all()


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )