import re
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from database import db
from services.normalization_services import normalize_to_frontend

# Model for table matches
class Matches(db.Model):
   winner_id = db.Column(db.String(7), db.ForeignKey('players.player_id'), primary_key=True)
   loser_id = db.Column(db.String(7), db.ForeignKey('players.player_id'), primary_key=True)
   tourney_date = db.Column(db.Date, primary_key=True)
   tourney_name = db.Column(db.String(35))
   surface = db.Column(db.String(8))
   tourney_level = db.Column(db.String(15))
   score = db.Column(db.String(50))
   best_of = db.Column(db.String(8))
   round_ = db.Column('round', db.String(23))
   w_aces = db.Column(db.String(8))
   w_df = db.Column(db.String(8))
   w_svpt = db.Column(db.String(8))
   w_1stIn = db.Column(db.String(8))
   w_1stWon = db.Column(db.String(8))
   w_2ndWon = db.Column(db.String(8))
   w_SvGms = db.Column(db.String(8))
   w_bpSaved = db.Column(db.String(8))
   w_bpFaced = db.Column(db.String(8))
   l_aces = db.Column(db.String(8))
   l_df = db.Column(db.String(8))
   l_svpt = db.Column(db.String(8))
   l_1stIn = db.Column(db.String(8))
   l_1stWon = db.Column(db.String(8))
   l_2ndWon = db.Column(db.String(8))
   l_SvGms = db.Column(db.String(8))
   l_bpSaved = db.Column(db.String(8))
   l_bpFaced = db.Column(db.String(8))
   year = db.Column(db.String(4))
   court = db.Column(db.String(8))
     
   winner = db.relationship('Players', foreign_keys=[winner_id], back_populates='matches_won')
   loser = db.relationship('Players', foreign_keys=[loser_id], back_populates='matches_lost')
   
   @hybrid_property
   def tourney_slug(self):
      # Converts tourney_name into a slug to use in Python
      # Replaces parts of the text that accomplish with the given pattern: one or more spaces
      return re.sub(r'\s+', '-', self.tourney_name.lower())
   
   @tourney_slug.expression
   def tourney_slug(cls):
      # Converts tourney_name into a slug in SQL
      # class method, not instance method
      # Mandatory if you want to use this attribute in SQL queries
      return func.lower(func.replace(cls.tourney_name, ' ', '-'))
   
   @hybrid_property
   def tourney_level_slug(self):
      # Converts tourney_level into a slug
      return re.sub(r'\s+', '-', self.tourney_level.lower())
   
   @tourney_level_slug.expression
   def tourney_level_slug(cls):
      # Converts tourney_level into a slug in SQL
      return func.lower(func.replace(cls.tourney_level, ' ', '-'))
    
   def to_dict(self):
   # Converts registers to dict and normalizes some values according to frontend

      matches_dict = {
         'winner_id': self.winner_id,
         'loser_id': self.loser_id,
         'winner_fullname': self.winner.fullname if self.winner else 'unknown',
         'loser_fullname': self.loser.fullname if self.loser else 'unknown',
         'winner_country': self.winner.country if self.winner else 'unknown',
         'loser_country': self.loser.country if self.loser else 'unknown',
         'tourney_date': self.tourney_date,
         'tourney_name': self.tourney_name,
         'tourney_slug': self.tourney_slug,
         'surface': self.surface,
         'tourney_level': self.tourney_level,
         'tourney_level_slug': self.tourney_level_slug,
         'score': self.score,
         'best_of': self.best_of,
         'round_': self.round_,
         'w_aces': self.w_aces,
         'w_df': self.w_df,
         'w_svpt': self.w_svpt,
         'w_1stIn': self.w_1stIn,
         'w_1stWon': self.w_1stWon,
         'w_2ndWon': self.w_2ndWon,
         'w_SvGms': self.w_SvGms,
         'w_bpSaved': self.w_bpSaved,
         'w_bpFaced': self.w_bpFaced,
         'l_aces': self.l_aces,
         'l_df': self.l_df,
         'l_svpt': self.l_svpt,
         'l_1stIn': self.l_1stIn,
         'l_1stWon': self.l_1stWon,
         'l_2ndWon': self.l_2ndWon,
         'l_SvGms': self.l_SvGms,
         'l_bpSaved': self.l_bpSaved,
         'l_bpFaced': self.l_bpFaced,
         'year': self.year,
         'court': self.court
      }
      
      return normalize_to_frontend(matches_dict)