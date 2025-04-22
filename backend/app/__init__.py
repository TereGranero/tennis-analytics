from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from config import DevelopmentConfig, ProductionConfig, TestingConfig
from .extensions import db, jwt
from .services.error_handlers import configure_error_handlers
from .api import init_api

# Loads enviroment variables from .env
load_dotenv()

def create_app():
   
   # Selects type of configuration
   flask_env = os.getenv('FLASK_ENV', 'development')
   if flask_env == 'production':
       config_class = ProductionConfig
   elif flask_env == 'testing':
       config_class = TestingConfig
   else:
       config_class = DevelopmentConfig
   
   # Instantiates flask app and loads configuration
   app = Flask(__name__)
   app.config.from_object(config_class)
   
   configure_error_handlers(app)
   
   # Configures CORS
   CORS(app, supports_credentials=True)
   
   # Initializes extensions
   db.init_app(app)
   jwt.init_app(app)
   
   # Initializes api
   init_api(app)
   
   return app
