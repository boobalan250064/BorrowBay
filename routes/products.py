from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from models import db
from models.product import Product

from sqlalchemy import or_

import os
import uuid


products = Blueprint(
    "products",
    __name__
)


# ==========================================
# ALLOWED IMAGE TYPES
# ==========================================

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
        and filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ==========================================
# SELLER PAGE
# ==========================================

@products.route("/seller")
@login_required
def seller_page():

    return render_template(
        "add_product.html"
    )


# ==========================================
# ADD / SELL PRODUCT
# ==========================================

@products.route(
    "/add-product",
    methods=["GET", "POST"]
)
@login_required
def add_product():

    if request.method == "POST":

        # ------------------------------
        # GET FORM DATA
        # ------------------------------

        name = request.form[
            "name"
        ].strip()

        description = request.form[
            "description"
        ].strip()

        category = request.form[
            "category"
        ].strip()

        price = request.form[
            "price"
        ]

        condition = request.form[
            "condition"
        ].strip()


        # ------------------------------
        # IMAGE
        # ------------------------------

        image = request.files.get(
            "image"
        )

        filename = None


        if image and image.filename:

            # Check image type

            if not allowed_file(
                image.filename
            ):

                flash(
                    "Only JPG, JPEG, PNG, GIF "
                    "and WEBP images are allowed."
                )

                return redirect(
                    url_for(
                        "products.add_product"
                    )
                )


            # Secure original filename

            original_name = secure_filename(
                image.filename
            )


            # Get extension

            extension = original_name.rsplit(
                ".",
                1
            )[1].lower()


            # Create unique filename

            filename = (
                str(uuid.uuid4())
                + "."
                + extension
            )


            # Upload folder

            upload_folder = os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(
                            __file__
                        )
                    )
                ),
                "uploads"
            )


            # Create folder if necessary

            os.makedirs(
                upload_folder,
                exist_ok=True
            )


            # Save image

            image.save(
                os.path.join(
                    upload_folder,
                    filename
                )
            )


        # ------------------------------
        # CREATE PRODUCT
        # ------------------------------

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


        db.session.add(
            product
        )

        db.session.commit()


        # ------------------------------
        # SUCCESS MESSAGE
        # ------------------------------

        flash(
            "Product successfully listed! "
            "It is now available on the Buyer page."
        )


        # Go to Buyer page

        return redirect(
            url_for(
                "products.browse_products"
            )
        )


    # GET request

    return render_template(
        "add_product.html"
    )


# ==========================================
# BUYER / PRODUCTS PAGE
# ==========================================

@products.route("/products")
@login_required
def browse_products():

    # Get search text from search bar

    search = request.args.get(
        "search",
        ""
    ).strip()


    # Start with available products

    query = Product.query.filter(
        Product.status == "available"
    )


    # ------------------------------
    # SEARCH
    # ------------------------------

    if search:

        search_text = (
            f"%{search}%"
        )


        query = query.filter(

            or_(

                Product.name.ilike(
                    search_text
                ),

                Product.category.ilike(
                    search_text
                ),

                Product.description.ilike(
                    search_text
                ),

                Product.condition.ilike(
                    search_text
                )

            )

        )


    # ------------------------------
    # GET PRODUCTS
    # ------------------------------

    product_list = query.order_by(
        Product.created_at.desc()
    ).all()


    # ------------------------------
    # SHOW BUYER PAGE
    # ------------------------------

    return render_template(

        "products.html",

        products=product_list,

        search=search

    )


# ==========================================
# PRODUCT DETAILS
# ==========================================

@products.route(
    "/product/<int:product_id>"
)
@login_required
def product_details(
    product_id
):

    product = Product.query.get_or_404(
        product_id
    )


    return render_template(

        "product_details.html",

        product=product

    )


# ==========================================
# MY LISTINGS
# ==========================================

@products.route(
    "/my-listings"
)
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