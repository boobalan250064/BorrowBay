from app import app
from models import db
from models.user import User
from models.product import Product


with app.app_context():

    # -----------------------------
    # DELETE OLD DATA
    # -----------------------------

    Product.query.delete()
    User.query.delete()

    db.session.commit()


    # -----------------------------
    # CREATE USERS
    # -----------------------------

    user1 = User(
        name="Arun",
        email="arun@gmail.com"
    )

    user1.set_password("123456")


    user2 = User(
        name="Ravi",
        email="ravi@gmail.com"
    )

    user2.set_password("123456")


    user3 = User(
        name="Kumar",
        email="kumar@gmail.com"
    )

    user3.set_password("123456")


    db.session.add_all([
        user1,
        user2,
        user3
    ])

    db.session.commit()


    # -----------------------------
    # CREATE PRODUCTS
    # -----------------------------

    product1 = Product(

        name="HP Laptop",

        description="HP laptop suitable for students and office work.",

        category="Electronics",

        price=35000,

        condition="Good",

        status="available",

        seller_id=user1.id
    )


    product2 = Product(

        name="Scientific Calculator",

        description="Casio scientific calculator for engineering students.",

        category="Education",

        price=800,

        condition="Good",

        status="available",

        seller_id=user2.id
    )


    product3 = Product(

        name="Bluetooth Speaker",

        description="Portable Bluetooth speaker with good sound quality.",

        category="Electronics",

        price=1500,

        condition="Like New",

        status="available",

        seller_id=user3.id
    )


    product4 = Product(

        name="Programming Book",

        description="Python programming book for beginners.",

        category="Books",

        price=450,

        condition="Good",

        status="available",

        seller_id=user1.id
    )


    product5 = Product(

        name="Study Table",

        description="Wooden study table suitable for students.",

        category="Furniture",

        price=2500,

        condition="Used",

        status="available",

        seller_id=user2.id
    )


    db.session.add_all([

        product1,

        product2,

        product3,

        product4,

        product5

    ])

    db.session.commit()


    print()
    print("================================")
    print("BorrowBay Demo Data Created!")
    print("================================")

    print()
    print("USERS")
    print("--------------------------------")

    print("Arun  : arun@gmail.com / 123456")
    print("Ravi  : ravi@gmail.com / 123456")
    print("Kumar : kumar@gmail.com / 123456")

    print()
    print("PRODUCTS")
    print("--------------------------------")

    print("HP Laptop")
    print("Scientific Calculator")
    print("Bluetooth Speaker")
    print("Programming Book")
    print("Study Table")

    print()
    print("================================")