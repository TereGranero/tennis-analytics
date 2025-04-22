from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# Model for table administrators
class Administrator(db.Model):
   __tablename__ = 'administrators'
   username = db.Column(db.String(100), primary_key=True)
   password = db.Column(db.String(100), nullable=False)
   
   def set_password(self, password):
      self.password = generate_password_hash(password)

   def check_password(self, password):
      return check_password_hash(self.password, password)
   