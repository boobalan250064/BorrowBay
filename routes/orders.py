from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models.order import Order
from models.product import Product
from models.cart import Cart


orders = Blueprint(
    "orders",
    __name__
)


# ==========================================
# BUY PRODUCT
# ==========================================

@orders.route(
    "/buy/<int:product_id>",
    methods=["GET", "POST"]
)
@login_required
def buy_product(product_id):

    product = Product.query.get_or_404(
        product_id
    )


    # --------------------------------------
    # SELLER CANNOT BUY OWN PRODUCT
    # --------------------------------------

    if product.seller_id == current_user.id:

        flash(
            "You cannot buy your own product."
        )

        return redirect(
            url_for(
                "products.browse_products"
            )
        )


    # --------------------------------------
    # PRODUCT MUST BE AVAILABLE
    # --------------------------------------

    if product.status != "available":

        flash(
            "This product is no longer available."
        )

        return redirect(
            url_for(
                "products.browse_products"
            )
        )


    # --------------------------------------
    # CREATE ORDER
    # --------------------------------------

    order = Order(

        product_id=product.id,

        buyer_id=current_user.id,

        seller_id=product.seller_id,

        price=product.price,

        status="Pending",

        order_type="Buy"

    )


    # --------------------------------------
    # MARK PRODUCT AS PENDING
    # --------------------------------------

    product.status = "pending"


    db.session.add(order)

    db.session.commit()


    # --------------------------------------
    # SUCCESS MESSAGE
    # --------------------------------------

    flash(
        "Order placed successfully!"
    )


    return redirect(
        url_for(
            "orders.my_orders"
        )
    )


# ==========================================
# MY ORDERS
# ==========================================

@orders.route(
    "/my-orders"
)
@login_required
def my_orders():

    order_list = Order.query.filter_by(

        buyer_id=current_user.id

    ).order_by(

        Order.id.desc()

    ).all()


    return render_template(

        "my_orders.html",

        orders=order_list

    )


# ==========================================
# ADD PRODUCT TO CART
# ==========================================

@orders.route(
    "/cart/add/<int:product_id>"
)
@login_required
def add_to_cart(product_id):

    product = Product.query.get_or_404(
        product_id
    )


    # --------------------------------------
    # USER CANNOT CART OWN PRODUCT
    # --------------------------------------

    if product.seller_id == current_user.id:

        flash(
            "You cannot add your own product to cart."
        )

        return redirect(
            url_for(
                "products.browse_products"
            )
        )


    # --------------------------------------
    # PRODUCT MUST BE AVAILABLE
    # --------------------------------------

    if product.status != "available":

        flash(
            "This product is no longer available."
        )

        return redirect(
            url_for(
                "products.browse_products"
            )
        )


    # --------------------------------------
    # CHECK IF ALREADY IN CART
    # --------------------------------------

    existing_item = Cart.query.filter_by(

        user_id=current_user.id,

        product_id=product.id

    ).first()


    if existing_item:

        flash(
            "This product is already in your cart."
        )

        return redirect(
            url_for(
                "products.browse_products"
            )
        )


    # --------------------------------------
    # ADD TO CART
    # --------------------------------------

    cart_item = Cart(

        user_id=current_user.id,

        product_id=product.id

    )


    db.session.add(
        cart_item
    )

    db.session.commit()


    flash(
        "Product added to your cart!"
    )


    return redirect(
        url_for(
            "products.browse_products"
        )
    )


# ==========================================
# MY CART
# ==========================================

@orders.route(
    "/cart"
)
@login_required
def cart():

    cart_items = Cart.query.filter_by(

        user_id=current_user.id

    ).order_by(

        Cart.id.desc()

    ).all()


    return render_template(

        "cart.html",

        cart_items=cart_items

    )


# ==========================================
# REMOVE FROM CART
# ==========================================

@orders.route(
    "/cart/remove/<int:cart_id>"
)
@login_required
def remove_from_cart(cart_id):

    cart_item = Cart.query.filter_by(

        id=cart_id,

        user_id=current_user.id

    ).first_or_404()


    db.session.delete(
        cart_item
    )

    db.session.commit()


    flash(
        "Product removed from cart."
    )


    return redirect(
        url_for(
            "orders.cart"
        )
    )