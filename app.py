# Importing essential dependencies
from flask import Flask, send_file, request, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required
# from security import authenticate, identity

from resources.HospitalResource import HospitalResource, HospitalListResource
from resources.RequestResource import RequestResource
from resources.DonationResource import DonationResource

# Initialize our flask application
app = Flask(__name__)

# Configuring SQL Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "jose"

# Initialize flask_restful Api
api = Api(app)

# Configuring token based authentication
# jwt = JWT(app, authenticate, identity) #/ auth
# Ask the db to create all the necessary tables before operation
# @app.before_first_request
# def create_tables():
#     db.create_all()

# Setting up a basic route for the homepage without using Flask-RESTful. This enables us to run our angular on the front end
@app.route("/")
def home():
    return send_file("templates/index.html")

api.add_resource(HospitalResource, "/hospital/<string:name>")
api.add_resource(HospitalListResource, "/hospitals")
api.add_resource(RequestResource, "/request/new")
api.add_resource(DonationResource, "/donation/new")

if __name__ == "__main__":
    # We import SQLAlchemy here from DB alchemy due to the problems with circular importsself.
    # Our models and in turn resources use SQL Alchemy, so we need to import the final version here
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
