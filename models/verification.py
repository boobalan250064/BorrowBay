from . import db


class PurchaseVerification(db.Model):

    __tablename__ = "purchase_verifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False,
        unique=True
    )

    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    address = db.Column(
        db.Text,
        nullable=False
    )

    city = db.Column(
        db.String(100),
        nullable=False
    )

    pincode = db.Column(
        db.String(10),
        nullable=False
    )

    aadhaar_last4 = db.Column(
        db.String(4),
        nullable=False
    )

    aadhaar_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    order = db.relationship(
        "Order",
        backref="verification",
        uselist=False
    )