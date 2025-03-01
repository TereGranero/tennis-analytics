from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db
from sqlalchemy import func, desc, extract
import os

from Services.wikidata_services import get_wikidata_enrichment              
from Services.normalization_services import normalize_into_db, normalize_to_frontend
from Services.validation_services import validate_request_data                            


# -------------------------- CONFIGURATION ---------------------------------- #

# Instanciates a Flask application
app = Flask(__name__) 

# Updates the application constantly
app.config.from_object(__name__) 

# Determines the database system used 
# and path to database relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] =  f"sqlite:///{os.path.abspath('tennisdb.sqlite')}"
#app.config['SQLALCHEMY_DATABASE_URI'] =  f"sqlite:///{os.path.abspath('testdb.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Inits database
db.init_app(app)

with app.app_context():
   from Models.Players import Players
   from Models.Rankings import Rankings
   from Models.Matches import Matches

# Enables CORS, the route and leave it open to other origins
CORS(app, resources={r"/*":{'origins':"*"}}) 

# ------------------------------- ROUTES ------------------------------------ #

# GET all players route handle
@app.route('/players', methods=['GET'])
def get_players():
   try:
      
      # Gets and validates arguments
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
      query = (
         base_query
         .order_by(desc(Players.birth_date))
         .offset((page - 1) * per_page)
         .limit(per_page)
      )
      
      # List of players objects
      players_objects_list = query.all()
      
      # List of players dicts to be sent in response
      players_list_in_page = []
      
      
      for player_object in players_objects_list:
         
         player_dict = player_object.to_dict()         
          
         # Enriches missing data with Wikidata
         update_flag, player_enriched = get_wikidata_enrichment(player_dict)
         
         # Commits changes into database
         if update_flag:
            
            player_normalized_into_db = normalize_into_db(player_enriched)
            
            # Updates player object
            player_object.name_first = player_normalized_into_db['name_first']
            player_object.name_last = player_normalized_into_db['name_last']
            player_object.hand = player_normalized_into_db['hand']
            player_object.birth_date = player_normalized_into_db['birth_date']
            player_object.country = player_normalized_into_db['country']
            player_object.height = player_normalized_into_db['height']
            player_object.wikidata_id = player_normalized_into_db['wikidata_id']
            player_object.fullname = player_normalized_into_db['fullname']
            player_object.weight = player_normalized_into_db['weight']
            player_object.instagram = player_normalized_into_db['instagram']
            player_object.facebook = player_normalized_into_db['facebook']
            player_object.x_twitter = player_normalized_into_db['x_twitter']
            player_object.pro_since = player_normalized_into_db['pro_since']
            
            db.session.commit()
            
            # Normalizes into frontend
            player_normalized_to_frontend = normalize_to_frontend(player_enriched)
            players_list_in_page.append(player_normalized_to_frontend)
         
         else:
            players_list_in_page.append(player_dict)   
               
      
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
def add_player():
   try:
      data = request.get_json()
      
      # Validates request data
      if not ( validate_request_data(data, 'POST')):         
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
      if not ( validate_request_data(data, 'PUT')):
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


if __name__ == "__main__":
   app.run(debug=True) #development mode
   