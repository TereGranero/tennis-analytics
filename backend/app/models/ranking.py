from app.extensions import db
from app.services.normalization_services import normalize_to_frontend


# Model for table rankings
class Ranking(db.Model):
   __tablename__ = 'rankings'
   player_id = db.Column(db.String(7), db.ForeignKey('players.player_id'), primary_key=True)
   ranking_date = db.Column(db.Date, primary_key=True)
   points = db.Column(db.String(7), nullable=False)
   rank = db.Column(db.Integer, nullable=False)

   
   # se accede así: ranking.fullname siendo ranking el resultado de una consulta a Ranking
   @property
   def fullname(self):
   # Returns player fullname corresponding to the ranking register player_id
      return self.player.fullname if self.player else 'unknown'
   
   @property
   def country(self):
   # Returns player country corresponding to the ranking register player_id
      return self.player.country if self.player else 'unknown'
   
   @property
   def name_last(self):
   # Returns player last name corresponding to the ranking register player_id
      return self.player.name_last if self.player else 'unknown'
   
   @property
   def name_first(self):
   # Returns player first name corresponding to the ranking register player_id
      return self.player.name_first if self.player else 'unknown'
     

   def to_dict(self):
      # Converts registers to dict and normalizes some values according to frontend      
      
      ranking_dict = {
         'player_id': self.player_id,
         'ranking_date': self.ranking_date,
         'points': self.points,
         'rank': self.rank,
         'fullname': self.fullname,
         'name_last': self.name_last,
         'name_first': self.name_first,
         'country': self.country
      }
      
      return normalize_to_frontend(ranking_dict)
   
