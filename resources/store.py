import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
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
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    # method to delete a specific store in the stores dictionary.
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store has been deleted."}
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    # many=True - Serializes each item in the list.
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()
    
    # blp argument specifies the format what should be in the body of a network request.
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    # create an store in the stores list as long as it doesn't exist already
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}  # unpack store_data and combine with id
        stores[store_id] = store

        return store
