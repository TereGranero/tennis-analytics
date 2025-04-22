from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask import current_app, request
from marshmallow import Schema, fields,ValidationError
from werkzeug.security import check_password_hash
from app.models.administrator import Administrator

class AuthPostSchema(Schema):
   # Schema for post request
   username = fields.Str(required=True)
   password = fields.Str(required=True)

   
class AuthAPI(Resource):
   def __init__(self) -> None:
      super().__init__()
      self.post_schema = AuthPostSchema()
   
   def post(self):
      try:
         # Gets payload from request
         data = request.get_json()
         
         # Validates request data
         if not data:         
            error_msg = f'Error Authentication. Incomplete request.'
            print(error_msg)
            response_object = {
               'status': 'error', 
               'message': error_msg
            }
            return response_object, 400
         
         args = self.post_schema.load(data)
         
         username = args.get('username')
         password = args.get('password')

         # Verifies user credentials as administrator in database
         admin = Administrator.query.filter_by(username=username).first()

         if not admin or not check_password_hash(admin.password, password):
            error_msg = "Wrong administrator credentials"
            print(error_msg)
            response_object = {
               'status': 'error',
               'message': error_msg
            }
            return response_object, 401

         # Creates JWT
         access_token = create_access_token(
            identity=str(admin.username)
         )

         response_object = {
            'status': 'success',
            'message': 'JWT has been created successfully!',
            'access_token': access_token
         }
         return response_object, 200
      
      except ValidationError as e:
         missing = ', '.join(e.messages.keys())
         error_msg = f"Error Authentication. Incomplete request. Missing {missing}"
         current_app.logger.error(error_msg, exc_info=False)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 400

      except Exception as e:
         error_msg = f'Error: {str(e)}'
         current_app.logger.error(error_msg, exc_info=True)
         response_object = {
            'status': 'error',
            'message': error_msg
         }
         return response_object, 500
