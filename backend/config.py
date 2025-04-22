import os
from datetime import timedelta
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config:
   # General configuration
   ADMIN_SECRET_KEY = os.getenv('ADMIN_SECRET_KEY')
   JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
   JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
   JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=3)
   JWT_TOKEN_LOCATION = ["headers"]  
   JWT_HEADER_NAME = "Authorization"
   JWT_HEADER_TYPE = "Bearer"
   
   # Determines the database system used 
   # and path to database relative to the app instance folder
   BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Backend directory
   DATABASE_FILE = os.getenv('DATABASE_FILE')
   DATABASE_PATH = os.path.join(BASE_DIR, 'app', 'data', DATABASE_FILE)
   SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   

class DevelopmentConfig(Config):
   DEBUG = True

class ProductionConfig(Config):
   DEBUG = False

class TestingConfig(Config):
   DEBUG = True
   #TESTING = True
   TEST_DATABASE_FILE = os.getenv('TEST_DATABASE_FILE')
   BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Backend directory
   DATABASE_PATH = os.path.join(BASE_DIR, 'app', 'api', 'data', TEST_DATABASE_FILE)
   SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
