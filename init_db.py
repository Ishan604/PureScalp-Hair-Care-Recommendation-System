from app import app, db
from models import Doctor

# Create all tables based on the models defined in SQLAlchemy
with app.app_context():
    db.create_all()  # This will create the tables in the database

print("Database tables created successfully.")
