from flask import Flask
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

# app.py is the first file to be executed when the application starts.
# It initializes the Flask application and registers the blueprints for the API.

app = Flask(__name__)

#  configurations
app.config["PROPAGATE_EXCEPTIONS"] = True   # Show any hidden errors from Flask to the main application
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"  # Tells flask smorest to use swagger api documentation and share. link - e.g. 127.0.0.1:5000/swagger-ui
# the path to swagger
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)  # Use flask_smorest extension

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)
