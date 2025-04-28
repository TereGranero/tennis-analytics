from flask_restful import Resource
from flask import current_app, request
from sqlalchemy import func, desc

from app.extensions import db
from app.models.match import Match
from app.models.player import Player
from app.services.wikidata_services import get_wikidata_enrichment              
from app.services.normalization_services import normalize_into_db, normalize_to_frontend


class TournamentsAPI(Resource):  
      
   def get(self, 
      search_level_slug=None, 
      search_tournament_slug=None):
      
      # Handles GET requests depending on arguments and routes
      path = request.path

      if 'level' in path and 'titles' not in path and search_level_slug:
         return self.get_tournaments_by_level(search_level_slug)
      elif 'winners' in path and search_tournament_slug:
         return self.get_tournament_winners(search_tournament_slug)
      elif 'titles/level' in path and search_level_slug:
         return self.get_ranking_titles(search_level_slug)
      
      
   def get_ranking_titles(self, search_level_slug):
      """ Retrieves ranking players by number of titles for a given level
      Args:
         search_level_slug (str): level slug to filter
      Returns:
         (dict, int):
            - dict: JSON response object
               - 'status' (str): 'success' or 'error'
               - 'message' (str): Error or success message
               - 'winners' (list, optional): List of winners dictionaries
               - 'total_winners': (int, optional): Total number of winners (only on success)
               - 'page' (int, optional): Current page returned (only on success)
               - 'pages' (int, optional): Total number of pages (only on success)
            - int: HTTP status code 
      """
      
      # --------------- Parameters validation -------------------
      
      # Default values
      default_page = 1
      default_per_page = 10
      
      # Validates search_level_slug
      try:
         if not db.session.query(Match).filter_by(tourney_level_slug=search_level_slug).first():
            error_msg = f'Error retrieving tournaments: Level {search_level_slug} not found in database.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            }
            return response_object, 400
      
      except Exception as e:
         error_msg = f'Error retrieving tournaments with level {search_level_slug}: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return response_object, 500
      
      # Validates page
      try:
         page = int(request.args.get('page', default_page))
         if page < 1:
            page = default_page  
            
      except ValueError:
         page = default_page
         
      # Validates per_page
      try:
         per_page = int(request.args.get('per_page', default_per_page))
         if (per_page < 1) or (per_page > 30):
            per_page = default_per_page
            
      except ValueError:
         per_page = default_per_page
        
      # Ends validation ---------------------------------------------------
   
      try:
         
         # Counts titles by player
         subquery = (db.session
            .query(
               Match.winner_id,
               func.count(Match.winner_id).label('titles')
            )
            .filter(Match.tourney_level_slug == search_level_slug)
            .filter(Match.round_ == 'The Final')
            .group_by(Match.winner_id)
            .subquery()
         )
         
         base_query = (db.session
            .query(
               subquery.c.winner_id,
               subquery.c.titles,
               Player
            )
            .join(Player, Player.player_id == subquery.c.winner_id)
            .order_by(desc(subquery.c.titles))
         )
            
                  
         # Calculates the number of winners
         total_winners = base_query.distinct(subquery.c.winner_id).count()
         
         # Calculates number of pages for all winners
         total_pages = (total_winners + per_page - 1) // per_page
         
         if page > total_pages: 
            page = total_pages if total_pages > 0 else 1

         # Retrieves ranking winners for current page
         objects_list = (base_query
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
         )
         
         # List of winners dicts to be sent in response
         winners_list_in_page = []
         
         # Converts winner player objects to dicts with frontend format adding titles
         for winner_id, titles, player in objects_list:
            winner_dict = player.to_dict()
            winner_dict['titles'] = int(titles)
            
            # Converts into a short dict with only fields of interest
            winner_fields_of_interest = [
               'player_id',
               'name_first',
               'name_last',
               'country',
               'fullname',
               'titles'
            ]
            short_winner_dict = {key: winner_dict[key] for key in winner_fields_of_interest}
            
            # Enriches missing winner country with Wikidata
            if short_winner_dict['country'] == 'unknown':

               # Retrieves player object from database
               player_object = (db.session
                  .query(Player)
                  .filter_by(player_id=short_winner_dict['player_id'])
                  .first()
               )
               
               if player_object: 
                  
                  # Converts into a short dict with only fields of interest
                  player_dict = player_object.to_dict()
                  player_fields_of_interest = [
                     'player_id',
                     'name_first',
                     'name_last',
                     'country',
                     'wikidata_id'
                  ]
                  short_player_dict = {key: player_dict[key] for key in player_fields_of_interest}
                  
                  # Enriches
                  update_flag, player_enriched = get_wikidata_enrichment(short_player_dict)
                  short_winner_dict['country'] = player_enriched['country']
                  
                  if update_flag:
                     
                     # Normalizes into database
                     player_normalized_into_db = normalize_into_db(player_enriched)
               
                     # Updates player object
                     player_object.name_first = player_normalized_into_db['name_first']
                     player_object.name_last = player_normalized_into_db['name_last']
                     player_object.country = player_normalized_into_db['country']
                     player_object.wikidata_id = player_normalized_into_db['wikidata_id']
                     db.session.commit()
                     
                     # Normalizes into frontend
                     player_normalized_to_frontend = normalize_to_frontend(player_enriched)
                  
                     short_winner_dict['country'] = player_normalized_to_frontend['country']
               
            winners_list_in_page.append(short_winner_dict)
                  
         
         response_object = {
            'status':'success',
            'message': f'Ranking winners of {search_level_slug} have been retrieved successfully!',
            'winners': winners_list_in_page,
            'total_winners': total_winners, 
            'page': page,
            'pages': total_pages
         } 
         return response_object, 200
      
      except Exception as e:
         error_msg = f'Error retrieving winners of {search_level_slug}: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return response_object, 500
       

     
   def get_tournaments_by_level(self, search_level_slug):    
      """ Retrieves tournaments for a given level
      Args:
         search_level_slug (str): level slug to filter
      Returns:
         (dict, int):
            - dict: JSON response object
               - 'status' (str): 'success' or 'error'
               - 'message' (str): Error or success message
               - 'tournaments' (list, optional): List of tournaments names
               - 'total_tournaments': (int, optional): Total number of tournaments (only on success)
               - 'page' (int, optional): Current page returned (only on success)
               - 'pages' (int, optional): Total number of pages (only on success)
            - int: HTTP status code 
      """
      
      # --------------- Parameters validation -------------------
      
      # Default values
      default_page = 1
      default_per_page = 10
      
      # Validates search_level_slug
      try:
         if not db.session.query(Match).filter_by(tourney_level_slug=search_level_slug).first():
            error_msg = f'Error retrieving tournaments: Level {search_level_slug} not found in database.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            }
            return response_object, 400
      
      except Exception as e:
         error_msg = f'Error retrieving tournaments with level {search_level_slug}: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return response_object, 500
      
      # Validates page
      try:
         page = int(request.args.get('page', default_page))
         if page < 1:
            page = default_page  
            
      except ValueError:
         page = default_page
         
      # Validates per_page
      try:
         per_page = int(request.args.get('per_page', default_per_page))
         if (per_page < 1) or (per_page > 30):
            per_page = default_per_page
            
      except ValueError:
         per_page = default_per_page
        
      # Ends validation ---------------------------------------------------
      
      
      try:         
         
         # Unique tournaments with search_level_slug
         base_query = (db.session
            .query(Match.tourney_name)
            .filter(Match.tourney_level_slug == search_level_slug)
            .distinct()
            .order_by(Match.tourney_name)
         )
         
         # Calculates the number of tournaments filtered by search_level_slug
         total_tournaments = base_query.count()
         
         # Calculates number of pages for all filtered tournaments
         total_pages = (total_tournaments + per_page - 1) // per_page
         
         if page > total_pages: 
            page = total_pages if total_pages > 0 else 1

         # Retrieves tournaments for current page
         tournaments_objects_list = (base_query
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
         )
         
         # List of tournaments dicts to be sent in response
         tournaments_list_in_page = [tournament_object[0] for tournament_object in tournaments_objects_list]
         
         response_object = {
            'status':'success',
            'message': f'Tournaments with level {search_level_slug} have been retrieved successfully!',
            'tournaments': tournaments_list_in_page,
            'total_tournaments': total_tournaments, 
            'page': page,
            'pages': total_pages
         } 
         return response_object, 200
      
      except Exception as e:
         error_msg = f'Error retrieving tournaments with level {search_level_slug}: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return response_object, 500
   
  
   def get_tournament_winners(self, search_tournament_slug):
      """ Retrieves winners for a given tournament
      Args:
         search_tournament_slug (str): tournament slug to filter
      Returns:
         (dict, int):
            - dict: JSON response object
               - 'status' (str): 'success' or 'error'
               - 'message' (str): Error or success message
               - 'winners' (list, optional): List of winners dictionaries
               - 'total_winners': (int, optional): Total number of winners (only on success)
               - 'page' (int, optional): Current page returned (only on success)
               - 'pages' (int, optional): Total number of pages (only on success)
            - int: HTTP status code 
      """
      
      # --------------- Parameters validation -------------------
         
      # Default values
      default_page = 1
      default_per_page = 10
      
      # Validates search_tournament_slug
      try:
         if not db.session.query(Match).filter_by(tourney_slug=search_tournament_slug).first():
            error_msg = f'Error retrieving winners: Tournament {search_tournament_slug} not found in database.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            }
            return response_object, 400
      
      except Exception as e:
         error_msg = f'Error retrieving winners for tournament {search_tournament_slug}: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return response_object, 500
      
      # Validates page
      try:
         page = int(request.args.get('page', default_page))
         if page < 1:
            page = default_page  
            
      except ValueError:
         page = default_page
         
      # Validates per_page
      try:
         per_page = int(request.args.get('per_page', default_per_page))
         if (per_page < 1) or (per_page > 30):
            per_page = default_per_page
            
      except ValueError:
         per_page = default_per_page
         
   # Ends validation ---------------------------------------------------
      
      try:
         
         # Retrieves all The Final matches for search_tournament_slug
         base_query = (db.session
            .query(Match)
            .filter(Match.tourney_slug == search_tournament_slug)
            .filter(Match.round_ == 'The Final')
            .order_by(desc(Match.year))
         )
         
         # Calculates the number of tournament editions/winners
         total_winners = base_query.count()
         
         # Calculates number of pages for all tournaments editions/winners
         total_pages = (total_winners + per_page - 1) // per_page
         
         if page > total_pages: 
            page = total_pages if total_pages > 0 else 1

         # Retrieves The Final matches for current page
         tournaments_objects_list = (base_query
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
         )
         
         # List of winners dicts to be sent in response
         winners_list_in_page = []
         
         # Converts objects to dicts with frontend format
         for tournament_object in tournaments_objects_list:
            winner_dict = tournament_object.to_dict()
            
            # Converts into a short dict with only fields of interest
            winner_fields_of_interest = [
               'tourney_name',
               'tourney_level',
               'year',
               'winner_id',
               'winner_fullname',
               'winner_country'
            ]
            short_winner_dict = {key: winner_dict[key] for key in winner_fields_of_interest}
            
            # Enriches missing winner country with Wikidata
            if short_winner_dict['winner_country'] == 'unknown':

               # Retrieves player object from database
               player_object = (db.session
                  .query(Player)
                  .filter_by(player_id=short_winner_dict['winner_id'])
                  .first()
               )
               
               if player_object: 
                  
                  # Converts into a short dict with only fields of interest
                  player_dict = player_object.to_dict()
                  player_fields_of_interest = [
                     'player_id',
                     'name_first',
                     'name_last',
                     'country',
                     'wikidata_id'
                  ]
                  short_player_dict = {key: player_dict[key] for key in player_fields_of_interest}
                  
                  # Enriches
                  update_flag, player_enriched = get_wikidata_enrichment(short_player_dict)
                  short_winner_dict['winner_country'] = player_enriched['country']
                  
                  if update_flag:
                     
                     # Normalizes into database
                     player_normalized_into_db = normalize_into_db(player_enriched)
               
                     # Updates player object
                     player_object.name_first = player_normalized_into_db['name_first']
                     player_object.name_last = player_normalized_into_db['name_last']
                     player_object.country = player_normalized_into_db['country']
                     player_object.wikidata_id = player_normalized_into_db['wikidata_id']
                     db.session.commit()
                     
                     # Normalizes into frontend
                     player_normalized_to_frontend = normalize_to_frontend(player_enriched)
                  
                     short_winner_dict['winner_country'] = player_normalized_to_frontend['country']
               
            winners_list_in_page.append(short_winner_dict)
                  
         
         response_object = {
            'status':'success',
            'message': f'Winners of {search_tournament_slug} have been retrieved successfully!',
            'winners': winners_list_in_page,
            'total_winners': total_winners, 
            'page': page,
            'pages': total_pages
         } 
         return response_object, 200

      
      except Exception as e:
         error_msg = f'Error retrieving winners of {search_tournament_slug}: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return response_object, 500
       
