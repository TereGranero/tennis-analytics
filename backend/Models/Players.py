from sqlalchemy import func, extract
from database import db

from Services.normalization_services import normalize_to_frontend
from Models.Rankings import Rankings 

# Model for table Players
class Players(db.Model):
   player_id = db.Column(db.String(7), primary_key=True)
   name_first = db.Column(db.String(50))
   name_last = db.Column(db.String(50))
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
   rankings = db.relationship('Rankings', backref='player', lazy='dynamic')
   
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
      return self.rankings.order_by(Rankings.rank.asc()).first()
   
   def get_all_rankings(self):
      # return array of dicts with 'player_id', 'ranking_date','points','rank'
      
      rankings_object_list = self.rankings.order_by(Rankings.ranking_date.asc()).all()
      rankings_list_in_player = []
      for ranking_object in rankings_object_list:
         ranking = ranking_object.to_dict()
         rankings_list_in_player.append(ranking)
      
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

    