from flask_restful import Resource
from flask import current_app, request
from sqlalchemy import desc
from marshmallow import Schema, fields, validates, ValidationError
import re

from app.extensions import db
from app.models.player import Player
from app.services.auth_services import auth_required
from app.services.wikidata_services import get_wikidata_enrichment              
from app.services.normalization_services import normalize_into_db, normalize_to_frontend


class PlayerPostPutSchema(Schema):
   
   # Schema for post/put request
   player_id = fields.Str(
      required=True, 
      error_messages={
        'required': 'player_id is required.',
        'invalid': 'player_id must be a string.'
      })
   name_first = fields.Str(
      required=True, 
      error_messages={
        'required': 'name_first is required.',
        'invalid': 'name_first must be a string.'
      })
   name_last = fields.Str(
      required=True, 
      error_messages={
        'required': 'name_last is required.',
        'invalid': 'name_last must be a string.'
      })
   hand = fields.Str(
      required=True, 
      error_messages={
        'required': 'hand is required.',
        'invalid': 'hand must be a string.'
      })
   birth_date = fields.Date(
      required=True, 
      error_messages={
        'required': 'birth_date is required.',
        'invalid': 'birth_date must be a string.'
      })
   country = fields.Str(
      required=True, 
      error_messages={
        'required': 'country is required.',
        'invalid': 'country must be a string.'
      })
   height = fields.Str(
      required=True, 
      error_messages={
        'required': 'height is required.',
        'invalid': 'height must be a string.'
      })
   wikidata_id = fields.Str(
      required=True, 
      error_messages={
        'required': 'wikidata_id is required.',
        'invalid': 'wikidata_id must be a string.'
      })
   fullname = fields.Str(
      required=True, 
      error_messages={
        'required': 'fullname is required.',
        'invalid': 'fullname must be a string.'
      })
   weight = fields.Str(
      required=True, 
      error_messages={
        'required': 'weight is required.',
        'invalid': 'weight must be a string.'
      })
   instagram = fields.Str(
      required=True, 
      error_messages={
        'required': 'instagram is required.',
        'invalid': 'instagram must be a string.'
      })
   facebook = fields.Str(
      required=True, 
      error_messages={
        'required': 'facebook is required.',
        'invalid': 'facebook must be a string.'
      })
   x_twitter = fields.Str(
      required=True, 
      error_messages={
        'required': 'x_twitter is required.',
        'invalid': 'x_twitter must be a string.'
      })
   pro_since = fields.Str(
      required=True, 
      error_messages={
        'required': 'pro_since is required.',
        'invalid': 'pro_since must be a string.'
      })
   
   # Validates some fields
   @validates('player_id')
   def validate_player_id(self, value):
      if len(value) < 3:
         raise ValidationError('player_id must have at least 3 chars.')
   
   @validates('name_last')
   def validate_name_last(self, value):
      if len(value) < 2:
         raise ValidationError('name_last must have at least 2 chars.')


class PlayersAPI(Resource):
   
   def __init__(self) -> None:
      super().__init__()
      self.post_put_schema = PlayerPostPutSchema()
      
      
   def get(self, player_id=None):
      if not player_id:
         if '/names' in request.path:
            # Extracts argument
            search_fullname = request.args.get('search_fullname', '').strip()
            return self.get_names(search_fullname)
         else:
            return self.get_all_players()
      elif request.path.endswith('/edit/' + player_id):
         return self.get_for_editing(player_id)
      else:
         return self.get_single_player(player_id)
      

   def get_names(self, search_fullname=''):
      
      # --------------- Parameters validation -------------------
      
      # Validates search_fullname
      try:

         if not search_fullname:
            error_msg = f'Error retrieving players: search_fullname is empty.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            }
            return response_object, 400
            
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
      
      
   def get_all_players(self):   
      # GET all players
      
      # --------------- Parameters validation -------------------
      
      # Default values
      default_page = 1
      default_per_page = 10
      default_name_last = ''
      
      # Validates search_name_last
      try:
         search_name_last = request.args.get('search_name_last', default_name_last).strip()
         
         # only alphanumerics
         if search_name_last and not search_name_last.isalnum():
            error_msg = f'Error retrieving players: search_name_last only accepts alphanumeric characters.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            }
            return response_object, 400
         
         # if exists en database
         if not db.session.query(Player).filter(Player.name_last.ilike(f'{search_name_last}%')).first():
            error_msg = f'Error retrieving players: Last name {search_name_last} not found in database.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            }
            return response_object, 400
      
      except Exception as e:
         error_msg = f'Error retrieving players with Last Name {search_name_last}: {str(e)}' if search_name_last else f'Error retrieving players: {str(e)}'
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
        
      # Ends validation -----------------------------------------------
            
      
      try:  
         
         # Retrieves all players in database
         base_query = db.session.query(Player)
         
         # Searches last names starting with search_name_last
         if search_name_last:
            base_query = base_query.filter(Player.name_last.ilike(f'{search_name_last}%'))

         # Calculates number of filtered players
         total_players = base_query.count()
         
         # Calculates number of pages for all filtered players
         total_pages = (total_players + per_page - 1) // per_page

         if page > total_pages: 
            page = total_pages if total_pages > 0 else 1

         # Retrieves filtered players for current page
         players_objects_list = (base_query
            .order_by(desc(Player.birth_date))
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
         )

         # List of players dicts to be sent in response
         players_list_in_page = []
         
         for player_object in players_objects_list:
         
            player_dict = player_object.to_dict()
            
            # Filters fields of interest
            fields_to_send = [
               'player_id', 
               'name_first', 
               'name_last', 
               'birth_date',
               'country', 
               'fullname', 
               'wikidata_id'
            ]
            short_player_dict = {key: player_dict[key] for key in fields_to_send}

            # Enriches missing data with Wikidata
            update_flag, player_enriched = get_wikidata_enrichment(short_player_dict)
            
            # Commits changes into database if any
            if update_flag:
               
               player_normalized_into_db = normalize_into_db(player_enriched)
               
               # Updates player object
               player_object.name_first = player_normalized_into_db['name_first']
               player_object.name_last = player_normalized_into_db['name_last']
               player_object.birth_date = player_normalized_into_db['birth_date']
               player_object.country = player_normalized_into_db['country']
               player_object.wikidata_id = player_normalized_into_db['wikidata_id']
               player_object.fullname = player_normalized_into_db['fullname']
               
               db.session.commit()
               
               # Normalizes into frontend
               player_normalized_to_frontend = normalize_to_frontend(player_enriched)
               players_list_in_page.append(player_normalized_to_frontend)
               
            else:
               players_list_in_page.append(short_player_dict)

         response_object = {
            'status': 'success',
            'message': 'Players have been retrieved successfully!',
            'players': players_list_in_page,
            'total_players': total_players,
            'page': page,
            'pages': total_pages
         }
         return response_object, 200

      except Exception as e:
         error_msg = f'Error retrieving players: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return response_object, 500


   def get_single_player(self, player_id):
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
         
         # Retrieves ranks by year and list of titles
         player_enriched['ranks_by_year'] = player_object.get_rank_by_year()  
         player_enriched['titles'] = player_object.get_titles()
         
         # Retrieves statistics
         player_enriched['best_ranking'] = player_object.get_best_ranking()
         player_enriched['total_titles'] = player_object.get_number_of_titles()
         player_enriched['grand_slams'] = player_object.get_number_of_titles('Grand Slam')
         player_enriched['masters1000'] = player_object.get_number_of_titles('Masters 1000')
         player_enriched['w_l'] = player_object.get_won_lost_ratio()
         player_enriched['aces'] = player_object.get_aces()
         player_enriched['aces_match'] = player_object.get_aces_by_match()
         player_enriched['double_faults'] = player_object.get_double_faults()
         player_enriched['double_faults_match'] = player_object.get_double_faults_by_match()
         player_enriched['points_on_first'] = player_object.get_points_on_first()
         player_enriched['points_on_first_match'] = player_object.get_points_on_first_by_match()
         player_enriched['games_on_serve'] = player_object.get_games_on_serve()
         player_enriched['games_on_serve_match'] = player_object.get_games_on_serve_by_match()
         player_enriched['first_in'] = player_object.get_first_in()
         player_enriched['first_in_match'] = player_object.get_first_in_by_match()
         player_enriched['bp_faced'] = player_object.get_faced_break_points()
         player_enriched['bp_saved_percentage'] = player_object.get_saved_break_points_percentage()
         
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

   @auth_required()
   def get_for_editing(self, player_id):
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
         
         player_dict = player_object.to_dict()
         
         response_object = {
            'status': 'success',
            'message': f'Player {player_id} has been retrieved successfully for editing!',
            'player': player_dict
         }
         return response_object, 200

      except Exception as e:
         error_msg = f'Error retrieving player {player_id} for editing: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 500
         
         
   @auth_required()
   def post(self):
      # POST new player
      
      try:
         # Gets payload from request
         data = request.get_json()
         
         # --------------- Parameters validation -------------------
         
         # Validates request data
         if not data:         
            error_msg = f'Error adding new player. Request with empty body.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            }
            return response_object, 400
         
         args = self.post_put_schema.load(data)
         
         # Validates player_id in case it already exists
         player_id = args['player_id']
         duplicated_player = Player.query.filter_by(player_id=player_id).first()
         
         if duplicated_player:
            error_msg = f'Error adding new player. Player with id {player_id} already exists.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            } 
            return response_object, 409
         
         # Ends validation -----------------------------------------------
         
         # Normalizes values into dababase
         new_player_normalized = normalize_into_db(args)

         # Creates new instance of model Player
         new_player_object = Player(**new_player_normalized)
         
         # Adds player
         db.session.add(new_player_object)
         
         # Commits changes into database
         db.session.commit()
         
         response_object = {
            'status': 'success', 
            'message': 'New player has been added successfully!'
         }
         return response_object, 201
      
      except ValidationError as err:
         error_messages = []
         
         for field, messages in err.messages.items():
            for msg in messages:
               if ('required' in msg) or ('invalid' in msg):
                  error_messages.append(f"{field}: {msg}")
               else:
                  error_messages.append(msg)
         
         if error_messages:
            if any('required' in msg or 'invalid' in msg for msg in error_messages):
               error_msg = "Error adding new player. Missing or invalid type in request: " + "; ".join(error_messages)
            else:
               error_msg = "Error adding new player. Validation failed: " + "; ".join(error_messages)
               
         current_app.logger.error(error_msg, exc_info=False)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 400
      
      except Exception as e:
         db.session.rollback()
         error_msg = f'Error adding new player: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return response_object, 500


   @auth_required()
   def delete(self, player_id=None):
      # DELETE player
      
      # No player_id
      if player_id is None:
         error_msg = "Error deleting player: No player id has been provided."
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 400
      
      try:
         # Retrieves player to update
         player = Player.query.filter_by(player_id=player_id).first()
         
         if not player:
            error_msg = f'Player id {player_id} not found in database.'
            print(error_msg)
            response_object = {
               'status': 'error',
               'message': error_msg
            }
            return response_object, 404

         # Deletes player
         db.session.delete(player)
         
         # Commits changes into database
         db.session.commit()
         
         response_object = {
            'status': 'success',
            'message': f'Player id {player_id} has been successfully deleted.'
         }
         return response_object, 200

      except Exception as e:
         error_msg = f'Error deleting player: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 500


   @auth_required()      
   def put(self, player_id=None):
      
      # No player_id
      if player_id is None:
         error_msg = "Error updating player: No player id has been provided."
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 400
      
      try:
         # Retrieves player to update
         player = Player.query.filter_by(player_id=player_id).first()

         if not player:
            error_msg = f'Player id {player_id} not found in database.'
            print(error_msg)
            response_object = {
               'status': 'error',
               'message': error_msg
            }
            return response_object, 404

         # Validates request data
         data = request.get_json()
         if not data:
            error_msg = f'Error updating player id {player_id}. Request with empty body.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            }
            return response_object, 400 
         
         args = self.post_put_schema.load(data)
         
         # Normalizes values into dababase
         player_normalized = normalize_into_db(args)
         
         # Updates player
         player.name_first = player_normalized['name_first']
         player.name_last = player_normalized['name_last']
         player.hand = player_normalized['hand']
         player.birth_date = player_normalized['birth_date']
         player.country = player_normalized['country']
         player.height = player_normalized['height']
         player.wikidata_id = player_normalized['wikidata_id']
         player.fullname = player_normalized['fullname']
         player.weight = player_normalized['weight']
         player.instagram = player_normalized['instagram']
         player.facebook = player_normalized['facebook']
         player.x_twitter = player_normalized['x_twitter']
         player.pro_since = player_normalized['pro_since']
         
         db.session.commit()
         
         response_object = {
            'status': 'success',
            'message': f'Player id {player_id} has been updated successfully!'
         }
         return response_object, 200
      
      except ValidationError as err:
         error_messages = []
         
         for field, messages in err.messages.items():
            for msg in messages:
               if ('required' in msg) or ('invalid' in msg):
                  error_messages.append(f"{field}: {msg}")
               else:
                  error_messages.append(msg)
         
         if error_messages:
            if any('required' in msg or 'invalid' in msg for msg in error_messages):
               error_msg = "Error updating player. Missing or invalid type in request: " + "; ".join(error_messages)
            else:
               error_msg = "Error updating player. Validation failed: " + "; ".join(error_messages)
               
         current_app.logger.error(error_msg, exc_info=False)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 400

      except Exception as e:
         db.session.rollback()
         error_msg = f'Error updating player: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 500
      