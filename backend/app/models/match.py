from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
import re
from app.services.normalization_services import normalize_to_frontend

# Model for table matches
class Match(db.Model):
   __tablename__ = 'matches'
   
   # -------------------------  Database columns ------------------------------
   
   winner_id = db.Column(db.String(7), db.ForeignKey('players.player_id'), primary_key=True)
   loser_id = db.Column(db.String(7), db.ForeignKey('players.player_id'), primary_key=True)
   tourney_date = db.Column(db.Date, primary_key=True)
   tourney_name = db.Column(db.String(35), nullable=False)
   surface = db.Column(db.String(8), nullable=False)
   tourney_level = db.Column(db.String(15), nullable=False)
   score = db.Column(db.String(50), nullable=False)
   best_of = db.Column(db.String(8), nullable=False)
   round_ = db.Column('round', db.String(23), nullable=False)
   w_aces = db.Column(db.String(8), nullable=False)
   w_df = db.Column(db.String(8), nullable=False)
   w_svpt = db.Column(db.String(8), nullable=False)
   w_1stIn = db.Column(db.String(8), nullable=False)
   w_1stWon = db.Column(db.String(8), nullable=False)
   w_2ndWon = db.Column(db.String(8), nullable=False)
   w_SvGms = db.Column(db.String(8), nullable=False)
   w_bpSaved = db.Column(db.String(8), nullable=False)
   w_bpFaced = db.Column(db.String(8), nullable=False)
   l_aces = db.Column(db.String(8), nullable=False)
   l_df = db.Column(db.String(8), nullable=False)
   l_svpt = db.Column(db.String(8), nullable=False)
   l_1stIn = db.Column(db.String(8), nullable=False)
   l_1stWon = db.Column(db.String(8), nullable=False)
   l_2ndWon = db.Column(db.String(8), nullable=False)
   l_SvGms = db.Column(db.String(8), nullable=False)
   l_bpSaved = db.Column(db.String(8), nullable=False)
   l_bpFaced = db.Column(db.String(8), nullable=False)
   year = db.Column(db.String(4), nullable=False)
   court = db.Column(db.String(8), nullable=False)
   
   
   # --------------------------  Relationships  -----------------------------
     
   winner = db.relationship('Player', foreign_keys=[winner_id], back_populates='matches_won')
   loser = db.relationship('Player', foreign_keys=[loser_id], back_populates='matches_lost')
   
   
   # -------------------------  Added Properties ------------------------------
   
   @property
   def winner_name_first(self):
      return self.winner.name_first if self.winner else 'unknown'
   
   @property
   def winner_name_last(self):
      return self.winner.name_last if self.winner else 'unknown'

   @property
   def winner_country(self):
      return self.winner.country if self.winner else 'unknown'
   
   @property
   def winner_fullname(self):
      return self.winner.fullname if self.winner else 'unknown'

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
   
   
   # ----------------------------  Methods ------------------------------------
    
   def to_dict(self):
   # Converts registers to dict and normalizes some values according to frontend

      matches_dict = {
         'winner_id': self.winner_id,
         'loser_id': self.loser_id,
         'winner_name_first': self.winner_name_first,
         'winner_name_last': self.winner_name_last,
         'winner_country': self.winner_country,
         'winner_fullname': self.winner_fullname,
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