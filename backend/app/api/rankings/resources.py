from flask_restful import Resource
from flask import current_app, request
from sqlalchemy import func, cast, Integer

from app.extensions import db
from app.models.ranking import Ranking
from app.models.player import Player
from app.services.wikidata_services import get_wikidata_enrichment              
from app.services.normalization_services import normalize_into_db, normalize_to_frontend


class RankingsAPI(Resource):
      
   def get(self, search_year=None):
      # GET rankings by year
      
      # --------------- Parameters validation -------------------
      
      # Default values
      default_page = 1
      default_per_page = 10
      default_year = '2023'
      
      # Validates search-year
      if search_year is None:
         search_year = default_year
         error_msg = "Warning retrieving rankings: No year has been provided. Default year will be retrieved."
         print(error_msg)
         
      else:
         try:
            search_year = int(search_year.strip())
            # out of range
            if (search_year < 1973) or (search_year > 2023):
               search_year = default_year
               error_msg = "Warning retrieving rankings: Provided year is out of records. Default year will be retrieved."
               print(error_msg)
            else:
               search_year = search_year
               
         except ValueError:
            search_year = default_year
            error_msg = "Warning retrieving rankings: Not valid year. Default year will be retrieved."
            print(error_msg)
     
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

         # Selects last-day-of-year date for selected year
         subquery = (db.session
            .query(func.max(Ranking.ranking_date))
            .filter(func.strftime('%Y', Ranking.ranking_date) == str(search_year))
            .scalar_subquery()  # to use inside filter
         )

         # End-of-year rankings by year. Query object
         base_query = (db.session
            .query(Ranking)
            .filter(Ranking.ranking_date == subquery)
            .order_by(cast(Ranking.rank, Integer))
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
                  .query(Player)
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
         return response_object, 200
      
      except Exception as e:
         error_msg = f'Error retrieving rankings: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error', 
            'message': error_msg
         }
         return response_object, 500
               