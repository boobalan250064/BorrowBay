from . import db


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    seller_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    image = db.Column(
        db.String(255)
    )

    condition = db.Column(
        db.String(50),
        default="Good"
    )

    status = db.Column(
        db.String(30),
        default="available"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    orders = db.relationship(
        "Order",
        backref="product",
        lazy=True
    )