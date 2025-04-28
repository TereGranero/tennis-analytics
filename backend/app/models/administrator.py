from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# Model for table administrators
class Administrator(db.Model):
   __tablename__ = 'administrators'
   username = db.Column(db.String(100), primary_key=True)
   password = db.Column(db.String(100), nullable=False)
   
   def set_password(self, password):
      """Generates a hashed password
      Args:
         password (str): given password
      Returns:
         (str): hashed password
      """
      self.password = generate_password_hash(password)

   def check_password(self, password):
      """Checks if provided password matches with saved hashed password
      Args:
         password (str): given password
      Returns:
         (bool): if given password is correct or not.
      """
      return check_password_hash(self.password, password)
   