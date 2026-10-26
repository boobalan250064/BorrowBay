from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

from models import db
from models.product import Product

import os
import uuid


products = Blueprint("products", __name__)


ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp"
}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@products.route("/seller")
@login_required
def seller_page():
    return render_template("add_product.html")


@products.route("/add-product", methods=["GET", "POST"])
@login_required
def add_product():

    if request.method == "POST":

        name = request.form["name"].strip()
        description = request.form["description"].strip()
        category = request.form["category"].strip()
        price = request.form["price"]
        condition = request.form["condition"].strip()

        image = request.files.get("image")

        filename = None

        # IMAGE UPLOAD
        if image and image.filename:

            if not allowed_file(image.filename):
                flash(
                    "Only JPG, JPEG, PNG, GIF and WEBP images are allowed."
                )
                return redirect(
                    url_for("products.add_product")
                )

            original_name = secure_filename(
                image.filename
            )

            extension = original_name.rsplit(
                ".",
                1
            )[1].lower()

            filename = (
                str(uuid.uuid4())
                + "."
                + extension
            )

            upload_folder = os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                ),
                "uploads"
            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            image.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )

        product = Product(
            name=name,
            description=description,
            category=category,
            price=float(price),
            condition=condition,
            image=filename,
            status="available",
            seller_id=current_user.id
        )

        db.session.add(product)
        db.session.commit()

        flash(
            "Product added successfully!"
        )

        return redirect(
            url_for(
                "products.browse_products"
            )
        )

    return render_template(
        "add_product.html"
    )


@products.route("/products")
@login_required
def browse_products():

    product_list = Product.query.filter_by(
        status="available"
    ).order_by(
        Product.id.desc()
    ).all()

    return render_template(
        "products.html",
        products=product_list
    )


@products.route("/product/<int:product_id>")
@login_required
def product_details(product_id):

    product = Product.query.get_or_404(
        product_id
    )

    return render_template(
        "product_details.html",
        product=product
    )


@products.route("/my-listings")
@login_required
def my_listings():

    product_list = Product.query.filter_by(
        seller_id=current_user.id
    ).order_by(
        Product.id.desc()
    ).all()

    return render_template(
        "my_listings.html",
        products=product_list
    )