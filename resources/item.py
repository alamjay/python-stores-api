import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
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
        item = ItemModel.query.get_or_404(item_id)
        return item

    # method to delete a specific item in the items dictionary.
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}, 200

    # blp argument specifies the format what should be in the body of a network request.
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    # updates a specific item in the dictionary. If it can't find the item then it'll return item not found.
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    # many=True - Serializes each item in the list.
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    # create an item in the items list as long as it doesn't exist already
    def post(self, item_data):
        # In the course, the guy removes the check as the database checks it anyways. But I believe you should keep this code.
        # The reason being the API can check to see if the item already exists before it reaches the final stage which is the database
        # It's an additional measurement to take. 

        existing_item = ItemModel.query.filter_by(name=item_data["name"]).first()
        if existing_item:
            abort(500, message=f"Item with name '{item_data['name']}' already exists.")

        # for item in items.values()
        #     if (
        #             item_data["name"] == item["name"]
        #             and item_data["store_id"] == item["store_id"]
        #     ):
        #         abort(400, message=f"Item already exists.")

        item = ItemModel(**item_data)
        print("item", item)

        db.session.add(item)
        db.session.commit()
        # try:
            
        # except SQLAlchemyError:
        #     abort(500, message="An error occurred while insterting the item.")

        ## code not longer needed
        # item_id = uuid.uuid4().hex
        # # **item_data is basically a spread operator, it unpacks the dictionary, 
        # #copies all the key-value pairs and then adds/overwrites the id with the value of item_id
        # item = {**item_data, "id": item_id}
        # items[item_id] = item

        return item
