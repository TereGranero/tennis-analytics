from flask import Blueprint
from flask_cors import CORS
from .auth import auth_bp
from .players import players_bp
from .rankings import rankings_bp
from .tournaments import tournaments_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')
CORS(api_bp, resources={r"/*": {"origins": "*"}})

def init_api(app):

   # sub-blueprints
   api_bp.register_blueprint(auth_bp, url_prefix='/auth', strict_slashes=False)
   api_bp.register_blueprint(players_bp, url_prefix='/players', strict_slashes=False)
   api_bp.register_blueprint(rankings_bp, url_prefix='/rankings', strict_slashes=False)
   api_bp.register_blueprint(tournaments_bp, url_prefix='/tournaments', strict_slashes=False)
   
   # main blueprint
   app.register_blueprint(api_bp)

