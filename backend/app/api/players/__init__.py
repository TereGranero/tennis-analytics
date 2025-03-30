from flask import Blueprint
from flask_restful import Api
from .resources import PlayersAPI

players_bp = Blueprint('players', __name__)
api = Api(players_bp)

api.add_resource(
   PlayersAPI, 
   '',
   '/', 
   '/<string:player_id>',
   '/edit/<string:player_id>',
   '/names',
)
