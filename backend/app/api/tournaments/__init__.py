from flask import Blueprint
from flask_restful import Api
from .resources import TournamentsAPI

tournaments_bp = Blueprint('tournaments', __name__)
api = Api(tournaments_bp)

api.add_resource(
   TournamentsAPI, 
   '/level/<string:search_level_slug>',
   '/winners/<string:search_tournament_slug>',
   '/titles/level/<string:search_level_slug>'  
)