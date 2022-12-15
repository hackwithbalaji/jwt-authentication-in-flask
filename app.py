from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from app_routes import Routes
from app_db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db.init_app(app)
Migrate(app, db)

api = Api(app)
Routes(api)

@app.route("/")
def home():
    return "Home page"
