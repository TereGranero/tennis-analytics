from functools import wraps
from flask_jwt_extended import verify_jwt_in_request

def auth_required():
   """ Creates a customized decorator to verify JWT
   Returns:
      function: 
   """
   
   def wrapper(fn):
      """ Decorator to be applied to protected functions
      Args:
         fn: decorator original function which is applied to protected functions
      Returns:
         function: decorator to be applied
      """
      
      @wraps(fn) # Decorated original function keeps its name and docstring.
      
      def decorator(*args, **kwargs):
         """ Creates customized function that verifies JWT token
         and returns customized error messages if any
         Returns:
            function: decorator original function if no exceptions
         """
         
         try:
            verify_jwt_in_request()
               
         except Exception as e:
            response_object = {
               'status': 'error',
               'message': 'Auth Services: Invalid or missing access token.'
            }
            return response_object, 401
         
         return fn(*args, **kwargs)
      
      return decorator
   
   return wrapper
