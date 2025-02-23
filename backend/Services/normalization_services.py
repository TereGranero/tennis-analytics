from datetime import datetime
import pycountry
import re


def normalize_to_frontend(player):
   
   for field, value in player.items():
      
      # Cleans strings
      value = value.strip() if (isinstance(value, str)) else value
   
      # Handles unknown values
      if ((not value or value == '-' or value == 'unknown') and field != 'birth_date'):
         player[field] = 'unknown' if (field == 'country') else '-'
         continue
      
      if (field == 'birth_date'):
         try:
            player[field] = value.strftime('%d-%m-%Y') if value else '01-01-1800'  
            
         except Exception as e:
            error_msg = f'Error converting birth_date {value}: {str(e)}'
            app.logger.error(error_msg, exc_info=True)
            player[field] = '01-01-1800'
         
      elif (field == 'country'):
         try:
            if (len(value) == 3):
               country = pycountry.countries.get(alpha_3=value.upper())
               player[field] = country.alpha_2.lower() if country else 'unknown'
            elif (len(value) == 2):
               country = pycountry.countries.get(alpha_2=value.upper())
               player[field] = country.alpha_2.lower() if country else 'unknown'
            else:
               player[field] = 'unknown'
         
         except Exception as e:
            error_msg = f'Error converting country: {value}: {str(e)}'
            app.logger.error(error_msg, exc_info=True)
            player[field] = 'unknown' 
      
      elif (field == 'hand'):
         hand_mapping_dict = {
            'r': 'Derecha',
            'l': 'Izquierda',
         }
         if (isinstance(value, str)):
            value = value.lower()
         player[field] = hand_mapping_dict.get(value, '-')
   
   return player    
    

def normalize_into_db(player):
   
   for field, value in player.items():
      
      # Cleans strings
      value = value.strip() if (isinstance(value, str)) else value
      
      # Handles unknown values
      if ((not value or value == '-' or value == 'unknown') and field != 'birth_date'):
         player[field] = 'unknown' 
         continue
      
      if (field == 'birth_date'):
         birth_date_formats = ['%Y-%m-%d', '%d-%m-%Y']
    
         if not value:
            player[field] = datetime.strptime('1800-01-01', '%Y-%m-%d').date()
         else:
            parsed = False
            for f in birth_date_formats:
               try:
                  player[field] = datetime.strptime(value, f).date()
                  parsed = True
                  break
               except ValueError:
                  continue
            
            if not parsed:
               error_msg = f'Error converting birth_date {value}'
               app.logger.error(error_msg, exc_info=True)
               player[field] = datetime.strptime('1800-01-01', '%Y-%m-%d').date()

      
      elif (field == 'country'):
         try:
            if (len(value) == 3):
               country = pycountry.countries.get(alpha_3=value.upper())
               player[field] = country.alpha_2.lower() if country else 'unknown'
            elif (len(value) == 2):
               country = pycountry.countries.get(alpha_2=value.upper())
               player[field] = country.alpha_2.lower() if country else 'unknown'
            else:
               player[field] = 'unknown'
         
         except Exception as e:
            error_msg = f'Error converting country {value}: {str(e)}'
            app.logger.error(error_msg, exc_info=True)
            player[field] = 'unknown'
            
      elif (field == 'hand'):
         hand_mapping_dict = {
            'derecha': 'R',
            'izquierda': 'L',
         }
         if (isinstance(value, str)):
            value = value.lower()
         player[field] = hand_mapping_dict.get(value, 'unknown')
      
         
      elif (field == 'height'):
         try:
            player[field] = (value if (isinstance(value, str) and 
                  int(value) > 100 and 
                  int(value) < 270) else 'unknown')
            
         except Exception as e:
            error_msg = f'Error in height {value}: {str(e)}'
            app.logger.error(error_msg, exc_info=True)
            player[field] = 'unknown'


      elif (field == 'weight'):
         try:
            player[field] = (value if (isinstance(value, str) and 
                  int(value) > 45 and 
                  int(value) < 150) else 'unknown')
            
         except Exception as e:
            error_msg = f'Error in weight {value}: {str(e)}'
            app.logger.error(error_msg, exc_info=True)
            player[field] = 'unknown'
            
            
      elif (field == 'pro_since'):
         try:
            player[field] = (value if (isinstance(value, str) and 
                  int(value) >= 1800 and 
                  int(value) <= datetime.now().year) else 'unknown')
            
         except Exception as e:
            error_msg = f'Error in pro_since {value}: {str(e)}'
            app.logger.error(error_msg, exc_info=True)
            player[field] = 'unknown'
            
                      
      elif (field in ['wikidata_id', 'name_first', 'name_last',
                      'instagram', 'facebook', 'x_twitter']):
         player[field] = (value if (isinstance(value, str) and  len(value) > 1) 
                          else 'unknown')
         
         
      elif (field == 'fullname'):
         # Just in case fullname is processed before name_first and name_last
         player['name_first'] = (player['name_first'].strip() if (isinstance(player['name_first'], str) and 
                                                                  len(player['name_first'].strip()) > 0) 
                                 else 'unknown')
         
         player['name_last'] = (player['name_last'].strip() if (isinstance(player['name_last'], str) and
                                                                len(player['name_last'].strip()) > 1) 
                                else 'unknown')
         
         # Checks if last name and first names are missing
         if (not player['name_last'] or 
            player['name_last'] == 'unknown' or 
            player['name_last'] == '-' ):
            player[field] = 'unknown'
         else:
            player[field] = (player['name_last'] if ( not player['name_first'] or 
                                                     player['name_first'] == 'unknown' or 
                                                     player['name_first'] == '-') 
                             else (player['name_last'] + ' ' + compose_initials(player['name_first']))
         )
 
   return player
   

def compose_initials(name):
   # Composes capital initials followed by dots, if needed
   # Used by normalize_fullname function
   
   name = name.strip()
   
   # Checks if name is already formatted as initials
   if (all(re.fullmatch(r"[A-Z](\.[A-Z])*\.", part) for part in name.split())):
      return name
   else:
      return ('.'.join(part[0].upper() for part in name.split()) + '.')

