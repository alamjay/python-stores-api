from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Str(dump_only=True) # dump_only=True means when we receive data and we pass that data through the Schema then you can't send name through
# the api, it can only be used to return data from the api
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)