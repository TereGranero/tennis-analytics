from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, verify_jwt_in_request
from config import Config
from dotenv import load_dotenv
from werkzeug.security import check_password_hash
from database import db
from sqlalchemy import func, desc, cast, Integer
from services.wikidata_services import get_wikidata_enrichment              
from services.normalization_services import normalize_into_db, normalize_to_frontend
from services.validation_services import validate_request_data                            


# -------------------------- CONFIGURATION ---------------------------------- #

# Loads enviroment variables from .env
load_dotenv()

# Instanciates a Flask application and configures
app = Flask(__name__) 
app.config.from_object(Config) 

# Inits JWT
jwt = JWTManager(app)

# Inits database
db.init_app(app)

with app.app_context():
   from models.Players import Players
   from models.Rankings import Rankings
   from models.Matches import Matches
   from models.Administrators import Administrators

# Enables CORS, the route and leave it open to other origins
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})


# ------------------------------- LOGIN ROUTE ------------------------------------ #

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token expirado"}), 401
 

@app.route('/login', methods=['POST'])
def login():
   try:
      data = request.get_json()
      if not data:
         error_msg = "Error login. No json data received"
         print(error_msg)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return jsonify(response_object), 400
         
      username = data.get('username')
      password = data.get('password')

   except Exception as e:
      error_msg = f"Error: {str(e)}"
      print(error_msg)
      response_object = {
         'status': 'error',
         'message': error_msg
      }
      return jsonify(response_object), 500
     
     
   # Verifies user credentials as administrator in database
   admin = Administrators.query.filter_by(username=username).first()

   if not admin or not check_password_hash(admin.password, password):
      error_msg = "Wrong administrator credentials"
      print(error_msg)
      response_object = {
         'status': 'error',
         'message': error_msg
      }
      return jsonify(response_object), 401

   # Creates JWT
   access_token = create_access_token(
      identity=str(admin.id)
   )
   
   response_object = {
      'status':'success',
      'message': 'JWT have been created successfully!',
      'access_token': access_token
   } 
   return jsonify(response_object), 200

      

# ------------------------------- PLAYER ROUTES ------------------------------------ #

# GET all players route handle
@app.route('/players', methods=['GET'])
def get_players():
   try:
      
      # Gets and validates url arguments
      page = int(request.args.get('page', 1))     
      per_page = int(request.args.get('per_page', 10))
      search_name_last = request.args.get('search_name_last', '').strip()
      
      if page < 1 : 
         page = 1
      
      if (per_page < 1 or per_page > 30): 
         per_page = 10
      
      # Retrieves all players in database
      base_query = db.session.query(Players)

      # Filters by search_name_last if provided
      if search_name_last:
         base_query = base_query.filter(Players.name_last.ilike(f'%{search_name_last}%'))

      # Calculates number of filtered players
      total_players = base_query.count()
      
      # Calculates number of pages for all filtered players
      total_pages = (total_players + per_page - 1) // per_page
      
      if page > total_pages: 
         page = total_pages if total_pages > 0 else 1
     
      # Retrieves filtered players for current page
      players_objects_list = (base_query
         .order_by(desc(Players.birth_date))
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
         
         # Commits changes into database
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
         'status':'success',
         'message': 'Players have been retrieved successfully!',
         'players': players_list_in_page,
         'total_players': total_players, 
         'page': page,
         'pages': total_pages
      } 
      
      return jsonify(response_object), 200
   
   except Exception as e:
      error_msg = f'Error retrieving players: {str(e)}'
      app.logger.error(error_msg, exc_info=True)
      response_object = {
         'status': 'error', 
         'message': error_msg
      }
      return jsonify(response_object), 500
      
      
# GET player by id for editing route handle
@app.route('/players/edit/<string:player_id>', methods=['GET'])
@jwt_required()
def get_player_for_editing(player_id):
   # No ranking data    
   
   try:
      player_object = Players.query.filter_by(player_id=player_id).first()

      if not player_object:
         error_msg = f'Player id {player_id} not found in database.'
         print(error_msg)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return jsonify(response_object), 404
      
      player_dict = player_object.to_dict()
      
      response_object = {
         'status': 'success',
         'message': f'Player {player_id} has been retrieved successfully!',
         'player': player_dict
      }
      return jsonify(response_object), 200

   except Exception as e:
      error_msg = f'Error retrieving player {player_id}: {str(e)}'
      app.logger.error(error_msg, exc_info=True)
      response_object = {
         'status': 'error',
         'message': error_msg
      }
      return jsonify(response_object), 500


# GET player by id route handle
@app.route('/players/<string:player_id>', methods=['GET'])
def get_player(player_id):
   try:
      player_object = Players.query.filter_by(player_id=player_id).first()

      if not player_object:
         error_msg = f'Player id {player_id} not found in database.'
         print(error_msg)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return jsonify(response_object), 404
      
      # Converts object to dict with frontend format
      player_dict = player_object.to_dict()
      
      # Enriches missing data with Wikidata
      update_flag, player_enriched = get_wikidata_enrichment(player_dict)
      
      # Retrieves ranks      
      player_enriched['ranks_by_year'] = player_object.get_rank_by_year()  
      
      # Best_rank
      player_enriched['best_ranking'] = player_object.get_best_ranking()
      
      # Number of titles won
      player_enriched['total_titles'] = player_object.get_number_of_titles()
      
      # W/L ratio
      player_enriched['w_l'] = player_object.get_won_lost_ratio()
      
      # Titles
      player_enriched['titles'] = player_object.get_titles()
      
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
      return jsonify(response_object), 200

   except Exception as e:
      error_msg = f'Error retrieving player {player_id}: {str(e)}'
      app.logger.error(error_msg, exc_info=True)
      response_object = {
         'status': 'error',
         'message': error_msg
      }
      return jsonify(response_object), 500


# POST player route handle
@app.route('/players', methods=['POST'])
@jwt_required()
def add_player():
   try:
      data = request.get_json()
      
      # Validates request data
      if not data or not (validate_request_data(data, 'POST')):         
         error_msg = f'Error adding new player. Incomplete request'
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return jsonify(response_object), 400
   
      
      # Normalizes values into dababase
      new_player_normalized = normalize_into_db(data)
      
      # Creates new instance of model Player
      new_player_object = Players(
         player_id = new_player_normalized['player_id'], 
         name_first = new_player_normalized['name_first'],
         name_last = new_player_normalized['name_last'],
         hand = new_player_normalized['hand'],
         birth_date = new_player_normalized['birth_date'],
         country = new_player_normalized['country'],
         height = new_player_normalized['height'],
         wikidata_id = new_player_normalized['wikidata_id'],
         fullname = new_player_normalized['fullname'],
         weight = new_player_normalized['weight'],
         instagram = new_player_normalized['instagram'],
         facebook = new_player_normalized['facebook'],
         x_twitter = new_player_normalized['x_twitter'],
         pro_since = new_player_normalized['pro_since']
      )
      
      # Adds player
      db.session.add(new_player_object)
      
      # Commits changes into database
      db.session.commit()
      
      response_object = {
         'status': 'success', 
         'message': 'New player has been added successfully!'
      }
      return jsonify(response_object), 201
   
   except Exception as e:
      db.session.rollback()
      error_msg = f'Error adding new player: {str(e)}'
      app.logger.error(error_msg, exc_info=True)
      response_object = {
         'status': 'error', 
         'message': error_msg
      }
      return jsonify(response_object), 500
      
# DELETE player route handle
@app.route('/players/<string:player_id>', methods=['DELETE'])
@jwt_required()
def delete_player(player_id):
   try:
      player = Players.query.filter_by(player_id=player_id).first()
      
      if not player:
         response_object = {
            'status': 'error',
            'message': f'Player id {player_id} not found in database.'
         }
         return jsonify(response_object), 404

      # Deletes player
      db.session.delete(player)
      
      # Commits changes into database
      db.session.commit()
      
      response_object = {
         'status': 'success',
         'message': f'Player id {player_id} has been successfully deleted.'
      }
      return jsonify(response_object), 200

   except Exception as e:
      error_msg = f'Error deleting player: {str(e)}'
      app.logger.error(error_msg, exc_info=True)
      response_object = {
         'status': 'error',
         'message': error_msg
      }
      return jsonify(response_object), 500

# PUT player by id route handle
@app.route('/players/<string:player_id>', methods=['PUT'])
@jwt_required()
def update_player(player_id):
   try:
      # Retrieves player to update
      player = Players.query.filter_by(player_id=player_id).first()

      if not player:
         response_object = {
            'status': 'error',
            'message': f'Player id {player_id} not found in database.'
         }
         return jsonify(response_object), 404

      data = request.get_json()
      
      # Validates request data
      if not data or not ( validate_request_data(data, 'PUT')):
         error_msg = f'Error updating player id {player_id}. Incomplete request'
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return jsonify(response_object), 400 
      
      # Normalizes values into dababase
      player_normalized = normalize_into_db(data)
      
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
      
      # Commits changes into database
      db.session.commit()
      
      response_object = {
         'status': 'success',
         'message': f'Player id {player_id} has been updated successfully!'
      }
      return jsonify(response_object), 200

   except Exception as e:
      db.session.rollback()
      error_msg = f'Error updating player: {str(e)}'
      app.logger.error(error_msg, exc_info=True)
      response_object = {
         'status': 'error',
         'message': error_msg
      }
      return jsonify(response_object), 500


# ------------------------------- RANKINGS ROUTES ------------------------------------ #

# GET rankings by year route handle
@app.route('/rankings/<string:search_year>', methods=['GET'])
def get_rankings_by_year(search_year):
   try:
      
      # Gets and validates arguments
      page = int(request.args.get('page', 1))     
      per_page = int(request.args.get('per_page', 10))
      
      if page < 1 : 
         page = 1
      
      if (per_page < 1 or per_page > 30): 
         per_page = 10
      
         
      # Selects last-day-of-year date for selected year
      subquery = (db.session
         .query(func.max(Rankings.ranking_date))
         .filter(func.strftime('%Y', Rankings.ranking_date) == str(search_year))
         .scalar_subquery()  # to use inside filter
      )

      # End-of-year rankings by year. Query object
      base_query = (db.session
         .query(Rankings)
         .filter(Rankings.ranking_date == subquery)
         .order_by(cast(Rankings.rank, Integer))
      )
      
      # Calculates the number of End-of-year rankings filtered by year
      total_rankings = base_query.count()
      
      # Calculates number of pages for all filtered rankings
      total_pages = (total_rankings + per_page - 1) // per_page
      
      if page > total_pages: 
         page = total_pages if total_pages > 0 else 1

      # Retrieves rankings for current page
      rankings_objects_list = (base_query
         .offset((page - 1) * per_page)
         .limit(per_page)
         .all()
      )
      
      # List of rankings dicts to be sent in response
      rankings_list_in_page = []
      
      # Converts objects to dicts with frontend format
      for ranking_object in rankings_objects_list:
         ranking_dict = ranking_object.to_dict()
         
         # Enriches missing country with Wikidata
         if ranking_dict['country'] == 'unknown':

            # Retrieves player object from database
            player_object = (db.session
               .query(Players)
               .filter_by(player_id=ranking_dict['player_id'])
               .first()
            )
            
            if player_object: 
               
               # Converts into a short dict with only fields of interest
               player_dict = player_object.to_dict()
               fields_of_interest = [
                  'player_id',
                  'name_first',
                  'name_last',
                  'country',
                  'wikidata_id'
               ]
               short_player_dict = {key: player_dict[key] for key in fields_of_interest}      

               # Enriches
               update_flag, player_enriched = get_wikidata_enrichment(short_player_dict)
               
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
               
                  ranking_dict['country'] = player_normalized_to_frontend['country']
                          
         rankings_list_in_page.append(ranking_dict)
               
      response_object = {
         'status':'success',
         'message': 'Rankings have been retrieved successfully!',
         'rankings': rankings_list_in_page,
         'total_rankings': total_rankings, 
         'page': page,
         'pages': total_pages
      } 
      return jsonify(response_object), 200
   
   except Exception as e:
      error_msg = f'Error retrieving rankings: {str(e)}'
      app.logger.error(error_msg, exc_info=True)
      response_object = {
         'status': 'error', 
         'message': error_msg
      }
      return jsonify(response_object), 500
      


# ------------------------------- TOURNAMENT ROUTES ------------------------------------ #

# GET tournaments by level route handle
@app.route('/tournaments/level/<string:search_level_slug>', methods=['GET'])
def get_tournaments_by_level(search_level_slug):
   try:
      
      # Gets and validates arguments
      page = int(request.args.get('page', 1))     
      per_page = int(request.args.get('per_page', 10))

      
      if page < 1 : 
         page = 1
      
      if (per_page < 1 or per_page > 30): 
         per_page = 10
         
      if not search_level_slug:
         search_level_slug = 'grand-slam'
      
         
      # Unique tournaments with search_level_slug
      base_query = (db.session
         .query(Matches.tourney_name)
         .filter(Matches.tourney_level_slug == search_level_slug)
         .distinct()
         .order_by(Matches.tourney_name)
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
      return jsonify(response_object), 200
   
   except Exception as e:
      error_msg = f'Error retrieving tournaments with level {search_level_slug}: {str(e)}'
      app.logger.error(error_msg, exc_info=True)
      response_object = {
         'status': 'error', 
         'message': error_msg
      }
      return jsonify(response_object), 500
   
   
# GET tournaments winners route handle
@app.route('/tournaments/winners/<string:search_tournament_slug>', methods=['GET'])
def get_tournament_winners(search_tournament_slug):
   try:
      
      # Gets and validates arguments
      page = int(request.args.get('page', 1))     
      per_page = int(request.args.get('per_page', 10))
      
      if page < 1 : 
         page = 1
      
      if (per_page < 1 or per_page > 30): 
         per_page = 10
      
         
      # Retrieves all The Final matches for search_tournament_slug
      base_query = (db.session
         .query(Matches)
         .filter(Matches.tourney_slug == search_tournament_slug)
         .filter(Matches.round_ == 'The Final')
         .order_by(desc(Matches.year))
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
               .query(Players)
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
      return jsonify(response_object), 200
   
   except Exception as e:
      error_msg = f'Error retrieving winners of {search_tournament_slug}: {str(e)}'
      app.logger.error(error_msg, exc_info=True)
      response_object = {
         'status': 'error', 
         'message': error_msg
      }
      return jsonify(response_object), 500
       

if __name__ == "__main__":
   app.run(debug=True) #development mode
   