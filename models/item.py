from db import db

# This file defines the ItemModel class, which represents the items table in the database.
# The db.Model class is a base class for all models in Flask-SQLAlchemy.
class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    # This creates a relationship between ItemModel and StoreModel class in SQLAlchemy.
    # Each ItemModel instance is linked to one StoreModel
    # back_populates="items" tells SQLAlchemy that the store should have corresponding items relationship that refers back to all items in that store
    # This enables to easily access item.store and all items from a store.items
    store = db.relationship("StoreModel", back_populates="items")
    # Adding relationship to the many-to-many table for tags_id in item_tags table
    tags = db.relationship("TagModel", back_populates="items", secondary="item_tags")
