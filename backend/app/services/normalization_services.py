from flask import current_app
from datetime import datetime, date
import pycountry
import re


def normalize_to_frontend(register):
   
   for field, value in register.items():
      
      # Cleans strings
      value = value.strip() if (isinstance(value, str)) else value
   
      # Handles unknown values
      if ((not value or value == '-' or value == 'unknown') and 'date' not in field):
         register[field] = 'unknown' if 'country' in field else '-'
         continue
      
      if ('date' in field):
         date_format_pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')
         if value and isinstance(value, str) and date_format_pattern.match(value):
            continue
         
         try:   
            register[field] = value.strftime('%d-%m-%Y') if hasattr(value, 'strftime') else '01-01-1800'  
            
         except Exception as e:
            error_msg = f'Error converting date {value}: {str(e)}'
            current_app.logger.error(error_msg, exc_info=True)
            register[field] = '01-01-1800'
         
      elif 'country' in field:
         try:
            if (len(value) == 3):
               country = pycountry.countries.get(alpha_3=value.upper())
               register[field] = country.alpha_2.lower() if country else 'unknown'
            elif (len(value) == 2):
               country = pycountry.countries.get(alpha_2=value.upper())
               register[field] = country.alpha_2.lower() if country else 'unknown'
            else:
               register[field] = 'unknown'
         
         except Exception as e:
            error_msg = f'Error converting country: {value}: {str(e)}'
            current_app.logger.error(error_msg, exc_info=True)
            register[field] = 'unknown' 
      
      elif (field == 'hand'):
         hand_mapping_dict = {
            'r': 'Derecha',
            'l': 'Izquierda',
         }
         if register[field] in hand_mapping_dict.values():  # Normalized
               continue
         if (isinstance(value, str)):
            register[field] = hand_mapping_dict.get(value.lower(), '-')
         
      elif (field == 'titles' and isinstance(value, list)):
         surface_mapping_dict = {
            'clay': 'Arcilla',
            'grass': 'Hierba',
            'hard': 'Dura', 
            'carpet': 'Moqueta'
         }
         for title in register[field]:
            surface = title.get('surface', '-')
            if surface in surface_mapping_dict.values():  # Normalized
               continue
            
            if (isinstance(surface, str)):
               title['surface'] = surface_mapping_dict.get(surface.lower(), '-')
   
   return register    
    

def normalize_into_db(register):
      
   for field, value in register.items():
      
      # Cleans strings
      value = value.strip() if (isinstance(value, str)) else value
      
      # Handles unknown values
      if ((not value or value == '-' or value == 'unknown') and 'date' not in field):
         register[field] = 'unknown' 
         continue
      
      if ('date' in field):
         date_formats = ['%Y-%m-%d', '%d-%m-%Y']

         # empty
         if not value:
            register[field] = datetime.strptime('1800-01-01', '%Y-%m-%d').date()

         else:
            # already date
            if isinstance(value, date):
               register[field] = value
            else:
               # is a string
               parsed = False
               for f in date_formats:
                  try:
                     register[field] = datetime.strptime(value, f).date()
                     parsed = True
                     break
                  except ValueError:
                     continue
               
               if not parsed:
                  error_msg = f'Error converting date {value}'
                  current_app.logger.error(error_msg, exc_info=True)
                  register[field] = datetime.strptime('1800-01-01', '%Y-%m-%d').date()

      
      elif ('country' in field):
         try:
            if (len(value) == 3):
               country = pycountry.countries.get(alpha_3=value.upper())
               register[field] = country.alpha_2.lower() if country else 'unknown'
            elif (len(value) == 2):
               country = pycountry.countries.get(alpha_2=value.upper())
               register[field] = country.alpha_2.lower() if country else 'unknown'
            else:
               register[field] = 'unknown'
         
         except Exception as e:
            error_msg = f'Error converting country {value}: {str(e)}'
            current_app.logger.error(error_msg, exc_info=True)
            register[field] = 'unknown'
            
      elif (field == 'hand'):
         hand_mapping_dict = {
            'derecha': 'R',
            'izquierda': 'L',
         }
         if (isinstance(value, str)):
            value = value.lower()
         register[field] = hand_mapping_dict.get(value, 'unknown')
      
         
      elif (field == 'height'):
         try:
            register[field] = (value if (isinstance(value, str) and 
                  int(value) > 100 and 
                  int(value) < 270) else 'unknown')
            
         except Exception as e:
            error_msg = f'Error in height {value}: {str(e)}'
            current_app.logger.error(error_msg, exc_info=True)
            register[field] = 'unknown'


      elif (field == 'weight'):
         try:
            register[field] = (value if (isinstance(value, str) and 
                  int(value) > 45 and 
                  int(value) < 150) else 'unknown')
            
         except Exception as e:
            error_msg = f'Error in weight {value}: {str(e)}'
            current_app.logger.error(error_msg, exc_info=True)
            register[field] = 'unknown'
            
            
      elif (field == 'pro_since'):
         try:
            register[field] = (value if (isinstance(value, str) and 
                  int(value) >= 1800 and 
                  int(value) <= datetime.now().year) else 'unknown')
            
         except Exception as e:
            error_msg = f'Error in pro_since {value}: {str(e)}'
            current_app.logger.error(error_msg, exc_info=True)
            register[field] = 'unknown'
            
                      
      elif (field in ['wikidata_id', 'name_first', 'name_last',
                      'instagram', 'facebook', 'x_twitter']):
         register[field] = (value if (isinstance(value, str) and  len(value) > 1) 
                          else 'unknown')
         
         
      elif (field == 'fullname'):
         # Just in case fullname is processed before name_first and name_last
         register['name_first'] = (register['name_first'].strip() if (isinstance(register['name_first'], str) and 
                                                                  len(register['name_first'].strip()) > 0) 
                                 else 'unknown')
         
         register['name_last'] = (register['name_last'].strip() if (isinstance(register['name_last'], str) and
                                                                len(register['name_last'].strip()) > 1) 
                                else 'unknown')
         
         # Checks if last name and first names are missing
         if (not register['name_last'] or 
            register['name_last'] == 'unknown' or 
            register['name_last'] == '-' ):
            register[field] = 'unknown'
         else:
            register[field] = (register['name_last'] if ( not register['name_first'] or 
                                                     register['name_first'] == 'unknown' or 
                                                     register['name_first'] == '-') 
                             else (register['name_last'] + ' ' + compose_initials(register['name_first']))
         )
 
   return register
   

def compose_initials(name):
   # Composes capital initials followed by dots, if needed
   # Used by normalize_fullname function
   
   name = name.strip()
   
   # Checks if name is already formatted as initials
   if (all(re.fullmatch(r"[A-Z](\.[A-Z])*\.", part) for part in name.split())):
      return name
   else:
      return ('.'.join(part[0].upper() for part in name.split()) + '.')

