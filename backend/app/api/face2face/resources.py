from flask_restful import Resource
from flask import current_app, request
from sqlalchemy import func, desc, cast, Integer
import re

from app.extensions import db
from app.models.player import Player
from app.models.ranking import Ranking
from app.models.match import Match

from app.services.wikidata_services import get_wikidata_enrichment              
from app.services.normalization_services import normalize_into_db, normalize_to_frontend


class Face2FaceAPI(Resource):  
   
   def get(self):
      if request.path.endswith('/names'):
         return self.get_names()
      
   # def get(self, player_id=None):
   #    if player_id:
   #       return self.get_statistics(player_id)
   #    elif not player_id and request.path.endswith('/name-players'):
   #       return self.get_names()
   
      
   def get_names(self):
      
      # --------------- Parameters validation -------------------
      
      # Default values
      default_fullname = ''
      
      # Validates search_fullname
      try:
         search_fullname = request.args.get('search_fullname', default_fullname).strip()
         
         # only alphanumerics
         if search_fullname and not re.match(r'^[a-zA-Z.\s]+$', search_fullname):
            error_msg = f'Error retrieving players: search_fullname only accepts letters, spaces and dots characters.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            }
            return response_object, 400
         
         # if exists en database
         if not db.session.query(Player).filter(Player.fullname.ilike(f'{search_fullname}%')).first():
            error_msg = f'Error retrieving players: Fullname starting with {search_fullname} not found in database.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            }
            return response_object, 400
      
      except Exception as e:
         error_msg = f'Error retrieving players with Fullname starting with {search_fullname}: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return response_object, 500
      
      # Ends validation -----------------------------------------------
      
      try:
         # Searches names starting with search_fullname
         query = (db.session
            .query(Player)
            .filter(Player.fullname.ilike(f'{search_fullname}%'))
            .all()
         )
         
         players = [
            {
               'player_id': player.player_id,
               'fullname': player.fullname
            }
            for player in query
         ]
         
         response_object = {
            'status': 'success',
            'message': 'Players names have been retrieved successfully!',
            'players': players
         }
         return response_object, 200
         
      except Exception as e:
         error_msg = f'Error retrieving players names: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 500
      
      
   # def get_statistics(self, player_id):
   #    try:
   #       player_object = Player.query.filter_by(player_id=player_id).first()

   #       if not player_object:
   #          error_msg = f'Player id {player_id} not found in database.'
   #          print(error_msg)
   #          response_object = {
   #             'status': 'error',
   #             'message': error_msg
   #          }
   #          return response_object, 404
         
   #       # Converts object to dict with frontend format
   #       player_dict = player_object.to_dict()
         
   #       # Enriches missing data with Wikidata
   #       update_flag, player_enriched = get_wikidata_enrichment(player_dict)
         
   #       # Retrieves ranks, best rank, number of titles won, W/L ratio and titles
   #       player_enriched['best_ranking'] = player_object.get_best_ranking()
   #       player_enriched['total_titles'] = player_object.get_number_of_titles()
   #       player_enriched['grand_slams'] = player_object.get_number_of_titles('Grand Slam')
   #       player_enriched['masters1000'] = player_object.get_number_of_titles('Masters 1000')       
   #       player_enriched['w_l'] = player_object.get_won_lost_ratio()
   #       player_enriched['aces'] = player_object.get_aces()
   #       player_enriched['aces_match'] = player_object.get_aces_by_match()
   #       player_enriched['double_faults'] = player_object.get_double_faults()
   #       player_enriched['double_faults_match'] = player_object.get_double_faults_by_match()
   #       player_enriched['points_on_first'] = player_object.get_points_on_first()
   #       player_enriched['points_on_first_match'] = player_object.get_points_on_first_by_match()
   #       player_enriched['games_on_serve'] = player_object.get_games_on_serve()
   #       player_enriched['games_on_serve_match'] = player_object.get_games_on_serve_by_match()
   #       player_enriched['first_in'] = player_object.get_first_in()
   #       player_enriched['first_in_match'] = player_object.get_first_in_by_match()
   #       player_enriched['bp_faced'] = player_object.get_faced_break_points()
   #       player_enriched['bp_saved_percentage'] = player_object.get_saved_break_points_percentage()
         
   #       # Commits changes into database
   #       if update_flag:
            
   #          # Normalizes data
   #          player_normalized = normalize_into_db(player_enriched)
            
   #          # Updates player object
   #          player_object.name_first = player_normalized['name_first']
   #          player_object.name_last = player_normalized['name_last']
   #          player_object.hand = player_normalized['hand']
   #          player_object.birth_date = player_normalized['birth_date']
   #          player_object.country = player_normalized['country']
   #          player_object.height = player_normalized['height']
   #          player_object.wikidata_id = player_normalized['wikidata_id']
   #          player_object.fullname = player_normalized['fullname']
   #          player_object.weight = player_normalized['weight']
   #          player_object.instagram = player_normalized['instagram']
   #          player_object.facebook = player_normalized['facebook']
   #          player_object.x_twitter = player_normalized['x_twitter']
   #          player_object.pro_since = player_normalized['pro_since']
            
   #          db.session.commit()
         
   #       player_dict = normalize_to_frontend(player_enriched)

   #       response_object = {
   #          'status': 'success',
   #          'message': f'Player {player_id} has been retrieved successfully!',
   #          'player': player_dict
   #       }
   #       return response_object, 200

   #    except Exception as e:
   #       error_msg = f'Error retrieving player {player_id}: {str(e)}'
   #       current_app.logger.error(error_msg, exc_info=True)
   #       response_object = {
   #          'status': 'error',
   #          'message': error_msg
   #       }
   #       return response_object, 500
