import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Adds backend directory (parent) to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from database import db
from models.Administrators import Administrators
from sqlalchemy import Column, Integer, String, MetaData, Table

with app.app_context():
   # Connects to dabase and gets schema
   engine = db.engine
   metadata = MetaData()
   metadata.reflect(bind=engine)

   # Creates table if not exists
   if 'administrators' not in metadata.tables:
      administrators = Table(
         'administrators', metadata,
         Column('id', Integer, primary_key=True, autoincrement=True),
         Column('username', String(50), nullable=False, unique=True),
         Column('password', String(50), nullable=False)
      )
      administrators.create(engine)
      print("Table 'administrators' has been created successfully.")
      
   else:
      print("Table 'administrators already exists.")

   # Inserts administrator if not exists
   if not Administrators.query.filter_by(username='tere').first():
      new_administrator = Administrators(id=1, username='tere')
      new_administrator.set_password(os.getenv('ADMIN_SECRET_KEY'))
      db.session.add(new_administrator)
      db.session.commit()
      print("Administrator 'tere' has been inserted succesfully.")
      
   else:
      print("Administrator 'tere' already exists.")
