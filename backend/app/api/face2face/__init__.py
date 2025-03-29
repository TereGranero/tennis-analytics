from flask import Blueprint
from flask_restful import Api
from .resources import Face2FaceAPI

face2face_bp = Blueprint('face2face', __name__)
api = Api(face2face_bp)

api.add_resource(
   Face2FaceAPI, 
   '/<string:player_id>',
   '/name-players'
)
