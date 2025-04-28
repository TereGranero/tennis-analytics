from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api
from .resources import AuthAPI

# Defines blueprint and associates resources and routes

auth_bp = Blueprint('auth', __name__)

CORS(auth_bp, resources={r"/*": {"origins": "*"}})

api = Api(auth_bp)

api.add_resource(
   AuthAPI, 
   '/', ''
)