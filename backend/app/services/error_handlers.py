from flask import jsonify

def configure_error_handlers(app):
   # Configures custom error handlers for app
   
   # 404 error
   @app.errorhandler(404)
   def not_found(error):
      error_msg = 'Requested URL is not valid on the server.'
      response_object = {
         'status': 'error',
         'message': error_msg
      }
      return jsonify(response_object), 404
