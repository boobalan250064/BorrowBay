from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db
from models.product import Product
from werkzeug.utils import secure_filename
import os
import os
import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)


products = Blueprint(
    "products",
    __name__
)


ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@products.route("/products")
def product_list():

    search = request.args.get(
        "search",
        ""
    ).strip()

    query = Product.query.filter_by(
        status="available"
    )

    if search:

        query = query.filter(
            Product.name.ilike(
                f"%{search}%"
            )
        )

    all_products = query.order_by(
        Product.created_at.desc()
    ).all()

    return render_template(
        "products.html",
        products=all_products,
        search=search
    )


@products.route("/product/<int:product_id>")
def product_details(product_id):

    product = Product.query.get_or_404(
        product_id
    )

    return render_template(
        "product_details.html",
        product=product
    )


@products.route("/add", methods=["GET", "POST"])
@login_required
def add_product():

    if request.method == "POST":

        name = request.form.get("name")

        description = request.form.get(
            "description"
        )

        category = request.form.get(
            "category"
        )

        condition = request.form.get(
            "condition"
        )

        price = request.form.get(
            "price"
        )

        image_name = None

        image = request.files.get(
            "image"
        )

        if image and image.filename:

            if allowed_file(
                image.filename
            ):

                extension = image.filename.rsplit(
                    ".",
                    1
                )[1].lower()

                image_name = (
                    str(uuid.uuid4())
                    + "."
                    + extension
                )

                filename = secure_filename(
                    image_name
                )

                image.save(
                    os.path.join(
                        current_app.config[
                            "UPLOAD_FOLDER"
                        ],
                        filename
                    )
                )

        product = Product(

            seller_id=current_user.id,

            name=name,

            description=description,

            category=category,

            condition=condition,

            price=float(price),

            image=image_name

        )

        db.session.add(product)

        db.session.commit()

        flash(
            "Product listed successfully!",
            "success"
        )

        return redirect(
            url_for(
                "products.my_listings"
            )
        )

    return render_template(
        "add_product.html"
    )


@products.route(
    "/product/<int:product_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_product(product_id):

    product = Product.query.get_or_404(
        product_id
    )

    if product.seller_id != current_user.id:

        flash(
            "You cannot edit this product.",
            "error"
        )

        return redirect(
            url_for(
                "products.product_list"
            )
        )

    if request.method == "POST":

        product.name = request.form.get(
            "name"
        )

        product.description = request.form.get(
            "description"
        )

        product.category = request.form.get(
            "category"
        )

        product.condition = request.form.get(
            "condition"
        )

        product.price = float(
            request.form.get("price")
        )

        db.session.commit()

        flash(
            "Product updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "products.my_listings"
            )
        )

    return render_template(
        "edit_product.html",
        product=product
    )


@products.route(
    "/product/<int:product_id>/delete",
    methods=["POST"]
)
@login_required
def delete_product(product_id):

    product = Product.query.get_or_404(
        product_id
    )

    if product.seller_id != current_user.id:

        flash(
            "You cannot delete this product.",
            "error"
        )

        return redirect(
            url_for(
                "products.my_listings"
            )
        )

    db.session.delete(product)

    db.session.commit()

    flash(
        "Product deleted.",
        "success"
    )

    return redirect(
        url_for(
            "products.my_listings"
        )
    )


@products.route("/my-listings")
@login_required
def my_listings():

    listings = Product.query.filter_by(
        seller_id=current_user.id
    ).order_by(
        Product.created_at.desc()
    ).all()

    return render_template(
        "my_listings.html",
        products=listings
    )
@products.route("/products")
@login_required
def browse_products():

    product_list = Product.query.filter_by(
        status="available"
    ).order_by(
        Product.created_at.desc()
    ).all()

    return render_template(
        "products.html",
        products=product_list
    )
@products.route("/seller")
@login_required
def seller_page():

    return render_template("add_product.html")
