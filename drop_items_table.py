from models import TagModel
from db import db
from app import app  # Adjust if your Flask app is named differently

with app.app_context():
    TagModel.__table__.drop(db.engine)
    print("'items' table dropped.")
