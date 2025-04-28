import sys
import os

# Adds backend directory (parent) to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run import app
from app.extensions import db
from app.models.administrator import Administrator
from sqlalchemy import Column, Integer, String, MetaData, Table

# Creates table administrator and inserts a unique registered administrator user
with app.app_context():
   # Connects to dabase and gets schema
   engine = db.engine
   metadata = MetaData()
   metadata.reflect(bind=engine)

   # Creates table if not exists
   if 'administrators' not in metadata.tables:
      administrators = Table(
         'administrators', metadata,
         Column('username', String(50), primary_key=True),
         Column('password', String(50), nullable=False)
      )
      administrators.create(engine)
      print("Table 'administrators' has been created successfully.")
      
   else:
      print("Table 'administrators already exists.")

   # Inserts administrator if not exists
   if not Administrator.query.filter_by(username='tere').first():
      new_administrator = Administrator(username='tere')
      new_administrator.set_password(os.getenv('ADMIN_SECRET_KEY'))
      db.session.add(new_administrator)
      db.session.commit()
      print("Administrator 'tere' has been inserted succesfully.")
      
   else:
      print("Administrator 'tere' already exists.")
