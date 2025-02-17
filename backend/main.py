from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, extract
import os
from datetime import datetime

from Services.wikidata_services import get_wikidata_id,\
                                       get_wikidata_country,\
                                       get_wikidata_birth_date, \
                                       get_wikidata_height, \
                                       get_wikidata_weight, \
                                       get_wikidata_hand, \
                                       compose_name_for_search
                                       
from Services.normalization_services import normalize_into_db
from Services.validation_services import validate_request_data
                                       
from Models.Players import Players
from Models.Rankings import Rankings


# -------------------------- CONFIGURATION ---------------------------------- #

# instanciates a Flask application
app = Flask(__name__) 
# updates the application constantly
app.config.from_object(__name__) 

# determines the database system used 
# and path to database relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] =  f"sqlite:///{os.path.abspath('tennisdb.sqlite')}"
# reduces terminal warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# We need: username, password, server location, database name. 

# enablse CORS, the route and leave it open to other origins
CORS(app, resources={r"/*":{'origins':"*"}}) 

# instantiates the database
db = SQLAlchemy(app)

   

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
      
      # Converts to list of dicts
      players_list_in_page = []
      
      # Composes dict for each player and searches missings in Wikidata
      #for player, best_rank in players_page:
      for player_object in players_objects_list:
         
         player = player_object.to_dict()         
         
         # Controls if commit is needed
         update_flag = False    

         # Gets wikidata id
         if player['wikidata_id'] == '-':
            
            # Composes complete player name to search its wikidata_id
            player_name = compose_name_for_search( 
               player['name_last'], 
               player['name_first']
            )
               
            wikidata_id = get_wikidata_id(player_name)
            if wikidata_id:
               player['wikidata_id'] = wikidata_id
               player_object.wikidata_id = wikidata_id 
               update_flag = True
         
         # Gets country
         if player['wikidata_id'] != '-' and player['country'] == 'unknown':
            
            country = get_wikidata_country(player['wikidata_id'])
            if country: 
               player['country'] = country
               player_object.country = country
               update_flag = True
               
         # Gets birth_date
         if player['wikidata_id'] != '-' and \
            ( player['birth_date'] == None or player['birth_date'] == '' or player['birth_date'] == '01-01-1800'):
            
            birth_date = get_wikidata_birth_date(player['wikidata_id'])
            if birth_date: 
               player['birth_date'] = birth_date.strftime('%d-%m-%Y') 
               player_object.birth_date = birth_date
               update_flag = True
            
         players_list_in_page.append(player)
         
         # Commits changes into database
         if update_flag:
            db.session.commit()
               
      
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
      
      player = player_object.to_dict()
      
      response_object = {
         'status': 'success',
         'message': f'Player {player_id} has been retrieved successfully!',
         'player': player
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
      
      player = player_object.to_dict()
      player['ranks_by_year'] = player_object.get_rank_by_year()  
      
      response_object = {
         'status': 'success',
         'message': f'Player {player_id} has been retrieved successfully!',
         'player': player
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
      player.name_first = player_normalized['name_first'],
      player.name_last = player_normalized['name_last'],
      player.hand = player_normalized['hand'],
      player.birth_date = player_normalized['birth_date'],
      player.country = player_normalized['country'],
      player.height = player_normalized['height'],
      player.wikidata_id = player_normalized['wikidata_id'],
      player.fullname = player_normalized['fullname'],
      player.weight = player_normalized['weight'],
      player.instagram = player_normalized['instagram'],
      player.facebook = normalize_into_db('facebook', data.get('facebook', 0)),
      player.x_twitter = player_normalized['x_twitter'],
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
   