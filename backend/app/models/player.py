from app.extensions import db
from sqlalchemy import func, extract, cast, Integer

from app.services.normalization_services import normalize_to_frontend
from .ranking import Ranking
from .match import Match

# Model for table players
class Player(db.Model):
   __tablename__ = 'players'
   player_id = db.Column(db.String(7), primary_key=True)
   name_first = db.Column(db.String(50), nullable=False)
   name_last = db.Column(db.String(50), nullable=False)
   hand = db.Column(db.String(7), nullable=False)
   birth_date = db.Column(db.Date, nullable=False)
   country = db.Column(db.String(3), nullable=False)
   height = db.Column(db.String(3), nullable=False)
   wikidata_id = db.Column(db.String(15), nullable=False)
   fullname = db.Column(db.String(60), nullable=False)
   weight = db.Column(db.String(3), nullable=False)
   instagram = db.Column(db.String(100), nullable=False)
   facebook = db.Column(db.String(100), nullable=False)
   x_twitter = db.Column(db.String(100), nullable=False)
   pro_since = db.Column(db.String(4), nullable=False)
   
   # Sets relationships with other models
   rankings = db.relationship('Ranking', backref='player', lazy='dynamic') 
   matches_won = db.relationship('Match', foreign_keys='Match.winner_id', back_populates='winner', lazy='dynamic')
   matches_lost = db.relationship('Match', foreign_keys='Match.loser_id', back_populates='loser', lazy='dynamic')
   
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
      """ Retrieves player's best ranking in career
      Returns:
         (int or str): best ranking if exists or '-'
      """
      
      best_ranking = self.rankings.with_entities(
         func.min(cast(Ranking.rank, Integer))
      ).scalar()

      if best_ranking:
         return best_ranking
      return '-'
   
   
   def get_all_rankings(self):
      """ Retrieves all player's ranking in career ordered by date
      Returns:
         (list of dict): dictionaries contain 'player_id', 'ranking_date','points','rank'
      """
            
      rankings_object_list = self.rankings.order_by(Ranking.ranking_date.asc()).all()
      rankings_list_in_player = []
      for ranking_object in rankings_object_list:
         ranking_dict = ranking_object.to_dict()
         rankings_list_in_player.append(ranking_dict)
      
      return rankings_list_in_player
   
   
   def get_rank_by_year(self):
      """ Retrieves player's end-of-season ATP rankings in career
      Returns:
         (list of dict): dictionaries contain 'year', 'rank'
      """

      # Groups rankings by year and retrieves last ranking by year. rankings takes all the columns, that is why uses with_entities
      subquery = self.rankings.with_entities(
         extract('year', Ranking.ranking_date).label('year'),    
         func.max(Ranking.ranking_date).label('max_date')
      ).group_by(extract('year', Ranking.ranking_date)).subquery()

      # Retrieves year and rank 
      # Filters rankings where ranking_date=max_date for each year
      query = self.rankings.join(   
         subquery,
         (Ranking.ranking_date == subquery.c.max_date)
      ).with_entities(       # selected columns
         subquery.c.year,
         Ranking.rank
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
      """ Retrieves all won matches
      Returns:
         (list of dict): won matches
      """
      matches_won = self.matches_won.all()
      
      return [match.to_dict() for match in matches_won]
   
      
   def get_matches_lost(self):
      """ Retrieves all lost matches
      Returns:
         (list of dict): lost matches
      """
      matches_lost = self.matches_lost.all()
      
      return [match.to_dict() for match in matches_lost]
   
   
   def get_total_matches(self):
      """ Retrieves number or total played matches
      Returns:
         (int): number of total played matches
      """
      total_matches_won = self.matches_won.count() 
      total_matches_lost = self.matches_lost.count()
      
      return total_matches_lost + total_matches_won
      
      
   def get_won_lost_ratio(self):
      """ Calculates victories versus looses ratio
      Returns:
         (float): won/lost ratio
      """
      total_matches_won = self.matches_won.count() 
      total_matches_lost = self.matches_lost.count()
      
      if (total_matches_lost == 0):  
         return 1 if (total_matches_won > 0) else 0
      
      return round(total_matches_won / total_matches_lost, 2)
      
   
   def get_titles(self, level=None):
      """ Retrieves won titles, filtering by level
      
      Args:
         level (optional): tourney level to filter
      
      Returns:
         (list of dict): won titles with provided level
      """
      
      titles = []

      # Filters won finals
      base_query = self.matches_won.filter_by(round_='The Final')
      
      # Filters by level if any
      if level:
         final_matches_object_list = base_query.filter_by(tourney_level=level).order_by(Match.tourney_date.desc()).all()
      else:
         final_matches_object_list = base_query.order_by(Match.tourney_date.desc()).all()

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
   
   
   def get_number_of_titles(self, level=None):
      """ Calculates number of won titles, filtering by level
      
      Args:
         level (optional): tourney level to filter
      
      Returns:
         (int): total won titles by provided level
      """
           
      # Filters won finals
      base_query = self.matches_won.filter_by(round_='The Final')
      
      # Filters by level if any
      if level:
         final_matches_object_list = base_query.filter_by(tourney_level=level).order_by(Match.tourney_date.desc()).all()
      else:
         final_matches_object_list = base_query.order_by(Match.tourney_date.desc()).all()

      return len(final_matches_object_list)
   
   
   def get_aces(self):
      """ Calculates number of aces in career
      
      Returns:
         (int): total aces in career
      """
      w_aces = db.session.query(
         func.sum(cast(Match.w_aces, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_aces = db.session.query(
         func.sum(cast(Match.l_aces, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      return w_aces + l_aces
   
   
   def get_aces_by_match(self):
      """ Calculates number of aces by match in career
      
      Returns:
         (float): aces ratio by match in career
      """
      w_aces = db.session.query(
         func.sum(cast(Match.w_aces, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_aces = db.session.query(
         func.sum(cast(Match.l_aces, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0
      
      total_matches = self.get_total_matches()
      if (total_matches == 0):
         return 0

      return round((w_aces + l_aces)/total_matches, 2)
   
   
   def get_double_faults(self):
      """ Calculates number of double faults in career
      
      Returns:
         (int): total double faults in career
      """
      w_df = db.session.query(
         func.sum(cast(Match.w_df, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_df = db.session.query(
         func.sum(cast(Match.l_df, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      return w_df + l_df
   
   
   def get_double_faults_by_match(self):
      """ Calculates number of double faults by match in career
      
      Returns:
         (float): double faults ratio by match in career
      """
      w_df = db.session.query(
         func.sum(cast(Match.w_df, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_df = db.session.query(
         func.sum(cast(Match.l_df, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0
      
      total_matches = self.get_total_matches()
      if (total_matches == 0):
         return 0
      
      return round((w_df + l_df)/total_matches, 2)
   
   
   def get_points_on_first(self):
      """ Calculates number of won points on first service in career
      
      Returns:
         (int): total won points on first service in career
      """
      w_1stWon = db.session.query(
         func.sum(cast(Match.w_1stWon, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_1stWon = db.session.query(
         func.sum(cast(Match.l_1stWon, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      return w_1stWon + l_1stWon
   
   
   def get_points_on_first_by_match(self):
      """ Calculates ratio of won points on first service by match in career
      
      Returns:
         (float): ratio of won points on first service by match in career
      """
      w_1stWon = db.session.query(
         func.sum(cast(Match.w_1stWon, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_1stWon = db.session.query(
         func.sum(cast(Match.l_1stWon, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      total_matches = self.get_total_matches()
      if (total_matches == 0):
         return 0
      
      return round((w_1stWon + l_1stWon)/total_matches, 2)
   
   
   def get_points_on_second(self):
      """ Calculates number of won points on second service in career
      
      Returns:
         (int): total won points on second service in career
      """
      w_2ndWon = db.session.query(
         func.sum(cast(Match.w_2ndWon, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_2ndWon = db.session.query(
         func.sum(cast(Match.l_2ndWon, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      return w_2ndWon + l_2ndWon
   
   
   def get_points_on_second_by_match(self):
      """ Calculates ratio of won points on second service by match in career
      
      Returns:
         (float): ratio of won points on second by match in career
      """
      w_2ndWon = db.session.query(
         func.sum(cast(Match.w_2ndWon, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_2ndWon = db.session.query(
         func.sum(cast(Match.l_2ndWon, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      total_matches = self.get_total_matches()
      if (total_matches == 0):
         return 0
      
      return round((w_2ndWon + l_2ndWon)/total_matches, 2)

   
   def get_games_on_serve(self):
      """ Calculates number of won games on service in career
      
      Returns:
         int: total won games on serve in career
      """
      w_SvGms = db.session.query(
         func.sum(cast(Match.w_SvGms, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_SvGms = db.session.query(
         func.sum(cast(Match.l_SvGms, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      return w_SvGms + l_SvGms
   
      
   def get_games_on_serve_by_match(self):
      """ Calculates ratio of won games on service by match in career
      
      Returns:
         (float): ratio of won games on serve by match in career
      """
      w_SvGms = db.session.query(
         func.sum(cast(Match.w_SvGms, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_SvGms = db.session.query(
         func.sum(cast(Match.l_SvGms, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      total_matches = self.get_total_matches()
      if (total_matches == 0):
         return 0
      
      return round((w_SvGms + l_SvGms)/total_matches, 2)
   
   
   
   def get_first_in(self):
      """ Calculates number of first-service-in in career
      
      Returns:
         (int): total first-service-in in career
      """
      w_1stIn = db.session.query(
         func.sum(cast(Match.w_1stIn, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_1stIn = db.session.query(
         func.sum(cast(Match.l_1stIn, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      return w_1stIn + l_1stIn
   
      
   def get_first_in_by_match(self):
      """ Calculates ratio of first service by match in in career
      
      Returns:
         (float): ratio of first service by match in in career
      """
      w_1stIn = db.session.query(
         func.sum(cast(Match.w_1stIn, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_1stIn = db.session.query(
         func.sum(cast(Match.l_1stIn, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      total_matches = self.get_total_matches()
      if (total_matches == 0):
         return 0
      
      
      return round((w_1stIn + l_1stIn)/total_matches, 2)

   

   def get_faced_break_points(self):
      """ Calculates number of faced break points in in career
      
      Returns:
         (int): total faced break points in career
      """
      w_bpFaced = db.session.query(
         func.sum(cast(Match.w_bpFaced, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_bpFaced = db.session.query(
         func.sum(cast(Match.l_bpFaced, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      return w_bpFaced + l_bpFaced
   
   def get_saved_break_points(self):
      """ Calculates number of saved break points in career
      
      Returns:
         int: total saved break points in career
      """
      w_bpSaved = db.session.query(
         func.sum(cast(Match.w_bpSaved, Integer))
      ).filter(Match.winner_id == self.player_id
               ).scalar() or 0

      l_bpSaved = db.session.query(
         func.sum(cast(Match.l_bpSaved, Integer))
      ).filter(Match.loser_id == self.player_id
               ).scalar() or 0

      return w_bpSaved + l_bpSaved
   
   def get_saved_break_points_percentage(self):
      """ Calculates percentage of saved break points in career
      
      Returns:
         (float): percentage of saved break points in career
      """
      bpSaved = self.get_saved_break_points()
      bpFaced = self.get_faced_break_points()
      if (bpFaced == 0):
         return 0
      
      return round((100 * bpSaved / bpFaced), 2)