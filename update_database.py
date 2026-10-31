from app import app
from models import db
from sqlalchemy import inspect, text


with app.app_context():

    inspector = inspect(db.engine)

    tables = inspector.get_table_names()

    if "products" not in tables:
        print("Products table does not exist.")
        print("Creating database tables...")

        db.create_all()

        print("Database tables created successfully.")

    else:

        columns = [
            column["name"]
            for column in inspector.get_columns("products")
        ]

        print("Existing columns:")
        print(columns)

        if "image" not in columns:

            print("Adding image column...")

            db.session.execute(
                text(
                    "ALTER TABLE products "
                    "ADD COLUMN image VARCHAR(255)"
                )
            )

            db.session.commit()

            print("Image column added successfully.")

        else:

            print("Image column already exists.")

        if "status" not in columns:

            print("Adding status column...")

            db.session.execute(
                text(
                    "ALTER TABLE products "
                    "ADD COLUMN status VARCHAR(30)"
                )
            )

            db.session.commit()

            print("Status column added successfully.")

        else:

            print("Status column already exists.")

print()
print("Database update completed.")