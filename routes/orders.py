from flask import (
    Blueprint,
    redirect,
    url_for,
    flash,
    render_template,
    request
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models.product import Product
from models.order import Order


orders = Blueprint(
    "orders",
    __name__
)


@orders.route(
    "/buy/<int:product_id>",
    methods=["POST"]
)
@login_required
def buy_product(product_id):

    product = Product.query.get_or_404(
        product_id
    )

    if product.seller_id == current_user.id:

        flash(
            "You cannot buy your own product.",
            "error"
        )

        return redirect(
            url_for(
                "products.product_details",
                product_id=product.id
            )
        )

    if product.status != "available":

        flash(
            "This product is no longer available.",
            "error"
        )

        return redirect(
            url_for(
                "products.product_details",
                product_id=product.id
            )
        )

    order_type = request.form.get(
        "order_type",
        "Buy"
    )

    order = Order(

        product_id=product.id,

        buyer_id=current_user.id,

        seller_id=product.seller_id,

        price=product.price,

        order_type=order_type,

        status="Pending"

    )

    product.status = "pending"

    db.session.add(order)

    db.session.commit()

    flash(
        "Order placed successfully!",
        "success"
    )

    return redirect(
        url_for(
            "orders.my_orders"
        )
    )


@orders.route("/my-orders")
@login_required
def my_orders():

    orders_list = Order.query.filter_by(
        buyer_id=current_user.id
    ).order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "my_orders.html",
        orders=orders_list
    )


@orders.route("/seller-orders")
@login_required
def seller_orders():

    orders_list = Order.query.filter_by(
        seller_id=current_user.id
    ).order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "dashboard.html",
        seller_orders=orders_list
    )


@orders.route(
    "/order/<int:order_id>/update",
    methods=["POST"]
)
@login_required
def update_order(order_id):

    order = Order.query.get_or_404(
        order_id
    )

    if order.seller_id != current_user.id:

        flash(
            "You cannot update this order.",
            "error"
        )

        return redirect(
            url_for(
                "orders.seller_orders"
            )
        )

    status = request.form.get(
        "status"
    )

    order.status = status

    if status == "Rejected":

        order.product.status = "available"

    elif status == "Accepted":

        order.product.status = "sold"

    db.session.commit()

    flash(
        "Order updated.",
        "success"
    )

    return redirect(
        url_for(
            "orders.seller_orders"
        )
    )