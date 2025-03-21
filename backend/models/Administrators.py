from database import db
from werkzeug.security import generate_password_hash, check_password_hash

# Model for table administrators
class Administrators(db.Model):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   username = db.Column(db.String(50), nullable=False, unique=True)
   password = db.Column(db.String(50), nullable=False)
   
   def set_password(self, password):
      self.password = generate_password_hash(password)

   def check_password(self, password):
      return check_password_hash(self.password, password)
   