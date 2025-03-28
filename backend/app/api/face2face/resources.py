from flask_restful import Resource
from flask import current_app, request
from sqlalchemy import func, desc, cast, Integer

from app.extensions import db
from app.models.player import Player
from app.models.ranking import Ranking
from app.models.match import Match

from app.services.wikidata_services import get_wikidata_enrichment              
from app.services.normalization_services import normalize_into_db, normalize_to_frontend


class Face2FaceAPI(Resource):  
      
   def get(self, player_id=None):
      if player_id:
         return self.get_statistics(player_id)
      elif not player_id and request.path.endswith('/top10-players'):
         return self.get_top10_names()
   
      
   def get_top10_names(self):
      try:
         # Calculates best rank for each player
         subquery = db.session.query(
            Ranking.player_id,
            func.min(cast(Ranking.rank, Integer)).label('best_rank')
         ).group_by(Ranking.player_id).subquery()
         
         # Filters players top 10
         query= db.session.query(
            Player
         ).join(
            subquery,
            Player.player_id == subquery.c.player_id
         ).filter(
            subquery.c.best_rank <= 10
         ).order_by(Player.fullname)
         
         top10_players = [
            {
               'player_id': player.player_id,
               'fullname': player.fullname
            }
            for player in query
         ]
         
         response_object = {
            'status': 'success',
            'message': 'Top 10 players names have been retrieved successfully!',
            'top10_players': top10_players
         }
         return response_object, 200
         
      except Exception as e:
         error_msg = f'Error retrieving Top 10 players names: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 500
      
      
   def get_statistics(self, player_id):
      try:
         player_object = Player.query.filter_by(player_id=player_id).first()

         if not player_object:
            error_msg = f'Player id {player_id} not found in database.'
            print(error_msg)
            response_object = {
               'status': 'error',
               'message': error_msg
            }
            return response_object, 404
         
         # Converts object to dict with frontend format
         player_dict = player_object.to_dict()
         
         # Enriches missing data with Wikidata
         update_flag, player_enriched = get_wikidata_enrichment(player_dict)
         
         # Retrieves ranks, best rank, number of titles won, W/L ratio and titles
         player_enriched['best_ranking'] = player_object.get_best_ranking()
         player_enriched['total_titles'] = player_object.get_number_of_titles()
         player_enriched['grand_slams'] = player_object.get_number_of_titles('Grand Slam')
         player_enriched['masters1000'] = player_object.get_number_of_titles('Masters 1000')       
         player_enriched['w_l'] = player_object.get_won_lost_ratio()
         player_enriched['aces'] = player_object.get_aces()
         player_enriched['double_faults'] = player_object.get_double_faults()
         player_enriched['points_on_first'] = player_object.get_points_on_first()
         player_enriched['points_on_second'] = player_object.get_points_on_second()
         player_enriched['games_on_serve'] = player_object.get_games_on_serve()
         player_enriched['first_in'] = player_object.get_first_in()
         player_enriched['bp_faced'] = player_object.get_faced_break_points()
         player_enriched['bp_saved'] = player_object.get_saved_break_points()
         
         # Commits changes into database
         if update_flag:
            
            # Normalizes data
            player_normalized = normalize_into_db(player_enriched)
            
            # Updates player object
            player_object.name_first = player_normalized['name_first']
            player_object.name_last = player_normalized['name_last']
            player_object.hand = player_normalized['hand']
            player_object.birth_date = player_normalized['birth_date']
            player_object.country = player_normalized['country']
            player_object.height = player_normalized['height']
            player_object.wikidata_id = player_normalized['wikidata_id']
            player_object.fullname = player_normalized['fullname']
            player_object.weight = player_normalized['weight']
            player_object.instagram = player_normalized['instagram']
            player_object.facebook = player_normalized['facebook']
            player_object.x_twitter = player_normalized['x_twitter']
            player_object.pro_since = player_normalized['pro_since']
            
            db.session.commit()
         
         player_dict = normalize_to_frontend(player_enriched)

         response_object = {
            'status': 'success',
            'message': f'Player {player_id} has been retrieved successfully!',
            'player': player_dict
         }
         return response_object, 200

      except Exception as e:
         error_msg = f'Error retrieving player {player_id}: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 500
