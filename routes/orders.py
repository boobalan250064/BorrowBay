from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from models import db
from models.order import Order
from models.product import Product


orders = Blueprint("orders", __name__)


@orders.route("/buy/<int:product_id>", methods=["POST"])
@login_required
def buy_product(product_id):

    product = Product.query.get_or_404(
        product_id
    )

    # Seller cannot buy their own product
    if product.seller_id == current_user.id:

        flash(
            "You cannot buy your own product."
        )

        return redirect(
            url_for(
                "products.browse_products"
            )
        )


    # Product must be available
    if product.status != "available":

        flash(
            "This product is no longer available."
        )

        return redirect(
            url_for(
                "products.browse_products"
            )
        )


    order = Order(
        product_id=product.id,

        buyer_id=current_user.id,

        seller_id=product.seller_id,

        price=product.price,

        status="Pending",

        order_type="Buy"
    )


    # Mark product as pending
    product.status = "pending"


    db.session.add(order)

    db.session.commit()


    flash(
        "Order placed successfully!"
    )


    return redirect(
        url_for(
            "orders.my_orders"
        )
    )


@orders.route("/my-orders")
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