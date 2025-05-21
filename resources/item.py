import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchema, ItemUpdateSchema

# This file defines the API endpoints for managing items in the store.

# This create a blueprint for the items resource.
blp = Blueprint("Items", __name__, description="Operations on items")


# This is the endpoint for a single item
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # blp response method is used to return the data with response status okay and in a format specified in ItemSchema.
    @blp.response(200, ItemSchema)
    # method to get item in the items dictionary and if it can't then it'll return item not found.
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    # method to delete a specific item in the items dictionary.
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item has been deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    # blp argument specifies the format what should be in the body of a network request.
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    # updates a specific item in the dictionary. If it can't find the item then it'll return item not found.
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data

            return item
        except KeyError:
            abort(404, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):
    # many=True - Serializes each item in the list.
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    # create an item in the items list as long as it doesn't exist already
    def post(self, item_data):
        for item in items.values():
            if (
                    item_data["name"] == item["name"]
                    and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists.")

        item_id = uuid.uuid4().hex
        # **item_data is basically a spread operator, it unpacks the dictionary, copies all the key-value pairs and then adds/overwrites the id with the value of item_id
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item
