from flask import Flask
from flask_restful import Api

from app_routes import Routes
from app_db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)
Routes(api)

@app.route("/")
def home():
    return "Home page"
