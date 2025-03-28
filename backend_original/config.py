import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
   ADMIN_SECRET_KEY = os.getenv('ADMIN_SECRET_KEY')
   JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
   JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
   JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=3)
   JWT_TOKEN_LOCATION = ["headers"]  
   JWT_HEADER_NAME = "Authorization"
   JWT_HEADER_TYPE = "Bearer"
   
   # Determines the database system used 
   # and path to database relative to the app instance folder
   DATABASE_FILE = os.getenv('DATABASE_FILE')
   SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.abspath(DATABASE_FILE)}"
   SQLALCHEMY_TRACK_MODIFICATIONS = False