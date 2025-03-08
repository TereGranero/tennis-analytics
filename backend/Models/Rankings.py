from database import db
from Services.normalization_services import normalize_to_frontend


# Model for table Rankings
class Rankings(db.Model):
   player_id = db.Column(db.String(7), db.ForeignKey('players.player_id'), primary_key=True)
   ranking_date = db.Column(db.Date, primary_key=True)
   points = db.Column(db.String(7))
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
     

   def to_dict(self):
      # Converts registers to dict and normalizes some values according to frontend      
      
      ranking_dict = {
         'player_id': self.player_id,
         'ranking_date': self.ranking_date,
         'points': self.points,
         'rank': self.rank,
         'fullname': self.fullname,
         'country': self.country
      }
      
      return normalize_to_frontend(ranking_dict)
   
