import os 
from flask import Flask
from flask_smorest import Api

from db import db
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

# app.py is the first file to be executed when the application starts.
# It initializes the Flask application and registers the blueprints for the API.

def create_app(db_url=None):
    app = Flask(__name__)

    #  configurations
    app.config["PROPAGATE_EXCEPTIONS"] = True   # Show any hidden errors from Flask to the main application
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"  # Tells flask smorest to use swagger api documentation and share. link - e.g. 127.0.0.1:5000/swagger-ui
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" # the path to swagger
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")  # SQLite database file
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable track modifications to save memory
    db.init_app(app)  # Initialize the database with the Flask app

    api = Api(app)  # Use flask_smorest extension

    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app

app = create_app()
