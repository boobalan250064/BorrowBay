from . import db


class Order(db.Model):

    __tablename__ = "orders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    buyer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    seller_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    order_type = db.Column(
        db.String(30),
        default="Buy"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    product = db.relationship(
        "Product",
        backref="orders"
    )

    buyer = db.relationship(
        "User",
        foreign_keys=[buyer_id]
    )

    seller = db.relationship(
        "User",
        foreign_keys=[seller_id]
    )