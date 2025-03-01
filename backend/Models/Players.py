from sqlalchemy import func, extract, cast, Integer
from database import db

from Services.normalization_services import normalize_to_frontend
from Models.Rankings import Rankings
from Models.Matches import Matches

# Model for table Players
class Players(db.Model):
   player_id = db.Column(db.String(7), primary_key=True)
   name_first = db.Column(db.String(50))
   name_last = db.Column(db.String(50), nullable=False)
   hand = db.Column(db.String(7))
   birth_date = db.Column(db.Date)
   country = db.Column(db.String(3))
   height = db.Column(db.String(3))
   wikidata_id = db.Column(db.String(15))
   fullname = db.Column(db.String(60))
   weight = db.Column(db.String(3))
   instagram = db.Column(db.String(100))
   facebook = db.Column(db.String(100))
   x_twitter = db.Column(db.String(100))
   pro_since = db.Column(db.String(4))
   
   # Sets relationships with other models
   rankings = db.relationship('Rankings', backref='player', lazy='dynamic') 
   matches_won = db.relationship('Matches', foreign_keys='Matches.winner_id', back_populates='winner', lazy='dynamic')
   matches_lost = db.relationship('Matches', foreign_keys='Matches.loser_id', back_populates='loser', lazy='dynamic')
   
   def to_dict(self):
      # Converts registers to dict and normalizes some values according to frontend
      
      player_dict = {
         'player_id': self.player_id,
         'name_first': self.name_first,
         'name_last': self.name_last,
         'hand': self.hand,
         'birth_date': self.birth_date,
         'country': self.country,
         'height': self.height,
         'wikidata_id': self.wikidata_id,
         'fullname': self.fullname,
         'weight': self.weight,
         'instagram': self.instagram,
         'facebook': self.facebook,
         'x_twitter': self.x_twitter,
         'pro_since': self.pro_since
      }
      
      return normalize_to_frontend(player_dict)
   

   def get_best_ranking(self):
      
      best_ranking = self.rankings.with_entities(
         func.min(cast(Rankings.rank, Integer))
      ).scalar()

      if best_ranking:
         return best_ranking
      return '-'
   
   
   def get_all_rankings(self):
      # return array of dicts with 'player_id', 'ranking_date','points','rank'
      
      rankings_object_list = self.rankings.order_by(Rankings.ranking_date.asc()).all()
      rankings_list_in_player = []
      for ranking_object in rankings_object_list:
         ranking_dict = ranking_object.to_dict()
         rankings_list_in_player.append(ranking_dict)
      
      return rankings_list_in_player
   
   
   def get_rank_by_year(self):

      # Groups rankings by year and retrieves last ranking by year
      subquery = self.rankings.with_entities(
         extract('year', Rankings.ranking_date).label('year'),    
         func.max(Rankings.ranking_date).label('max_date')
      ).group_by(extract('year', Rankings.ranking_date)).subquery()

      # Retrieves year and rank 
      # Filters rankings where ranking_date=max_date for each year
      query = self.rankings.join(   
         subquery,
         (Rankings.ranking_date == subquery.c.max_date)
      ).with_entities(       # selected columns
         subquery.c.year,
         Rankings.rank
      ).order_by(subquery.c.year)

      # Formats for echarts
      return [
         {
            'year': int(year),
            'rank': rank
         }
         for year, rank in query
      ]


   def get_matches_won(self):
      """
      Retrieves all won matches
      
      Returns:
         array: array of dict with won matches
      """
      matches_won = self.matches_won.all()
      
      return [match.to_dict() for match in matches_won]
   
      
   def get_matches_lost(self):
      """
      Retrieves all lost matches
      
      Returns:
         array: dicts with lost matches
      """
      matches_lost = self.matches_lost.all()
      
      return [match.to_dict() for match in matches_lost]
   
   
   def get_won_lost_ratio(self):
      """
      Calculates victories versus looses ratio
      
      Returns:
         float: won/lost ratio
      """
      total_matches_won = self.matches_won.count() 
      total_matches_lost = self.matches_lost.count()
      
      if (total_matches_lost == 0):  
         return 1 if (total_matches_won > 0) else 0
      
      return round(total_matches_won / total_matches_lost, 4)
      
   
   def get_titles(self):
      """
      Retrieves won titles
      
      Returns:
         array: a dict for each title
      """
      
      titles = []

      # Filters won finals
      final_matches_object_list = self.matches_won.filter_by(round_='The Final').order_by(Matches.tourney_date.desc()).all()

      # Appends to 
      for match_object in final_matches_object_list:
         match_dict = match_object.to_dict()
         titles.append({
            'tourney_name': match_dict['tourney_name'],
            'year': match_dict['year'],
            'surface': match_dict['surface'],
            'tourney_level': match_dict['tourney_level']
         })

      return titles
   
   
   def get_number_of_titles(self):
      """
      Calculates number of won titles
      
      Returns:
         int: total titles
      """
      
      # Filters won finals
      final_matches_object_list = self.matches_won.filter_by(round_ ='The Final').all()

      return len(final_matches_object_list)
   
   