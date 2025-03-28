from flask import Blueprint
from flask_restful import Api
from .resources import RankingsAPI

rankings_bp = Blueprint('rankings', __name__)
api = Api(rankings_bp)

api.add_resource(
   RankingsAPI, 
   '/<string:search_year>',
)