from database import db

# Model for table Rankings
class Rankings(db.Model):
   player_id = db.Column(db.String(7), db.ForeignKey('players.player_id'), primary_key=True)
   ranking_date = db.Column(db.Date, primary_key=True)
   points = db.Column(db.String(7))
   rank = db.Column(db.Integer)

   def to_dict(self):
      # Converts registers to dict and normalizes some values according to frontend
      
      def format_unknown(value):
         return value if value != "unknown" else "-"
            
      def normalize_points(points):
         return format_unknown(points)
      
      def format_ranking_date(ranking_date):
         if ranking_date: 
            return ranking_date.strftime('%d-%m-%Y') 
         return None
      
      return {
         'player_id': self.player_id,
         'ranking_date': format_ranking_date(self.ranking_date),
         'points': normalize_points(self.points),
         'rank': self.rank
      }