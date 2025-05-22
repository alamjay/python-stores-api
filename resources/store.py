import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

# This file defines the API endpoints for managing store

# This create a blueprint for the stores resource.
blp = Blueprint("Stores", __name__, description="Operations on stores")

# The endpoint for a single store
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    # blp response method is used to return the data with response status okay and in a format specified in StoreSchema.
    @blp.response(200, StoreSchema)
    # method to get store in the stores dictionary and if it can't then it'll return store not found.
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    # method to delete a specific store in the stores dictionary.
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}, 200
    
    # method to update a store in the stores dictionary.
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)

        if store:
            store.name = store_data["name"]
        else:
            store = StoreModel(id=store_id, **store_data)

        db.session.add(store)
        db.session.commit()

        return store


@blp.route("/store")
class StoreList(MethodView):
    # many=True - Serializes each item in the list.
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    # blp argument specifies the format what should be in the body of a network request.
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    # create an store in the stores list as long as it doesn't exist already
    def post(self, store_data):
        existing_store = StoreModel.query.filter_by(name=store_data["name"]).first()
        if existing_store:
            abort(400, message=f"Store with name '{store_data['name']}' already exists.")
        # for store in StoreModel.query.all():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message=f"Store already exists.")

        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError: 
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while insterting the item.")

        # store_id = uuid.uuid4().hex
        # store = {**store_data, "id": store_id}  # unpack store_data and combine with id
        # stores[store_id] = store

        return store
