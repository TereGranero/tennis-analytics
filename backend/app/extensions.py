from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Instantiates the database and jwt manager
db = SQLAlchemy()
jwt = JWTManager()

