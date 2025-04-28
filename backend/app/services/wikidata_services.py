import requests
from requests.exceptions import HTTPError, RequestException
from datetime import datetime
import time
from functools import lru_cache

BASE_SLEEP = 0.5  # seconds between requests
MAX_RETRIES = 3
MAX_ACCEPTABLE_WAIT = 10

# Memo cache to avoid repeated requests
@lru_cache(maxsize=128)

def get_wikidata_property(wikidata_id, property):
   """ Retrieves the requested property from a Wikidata entity using the MediaWiki Action API.

   Args:
      wikidata_id (str): Wikidata entity ID
      property (str): The requested property ID
      
   Returns:
      (list or None): A list of claims for the specified property 
                     or None if an error occurs or the property does not exist.
   """
   
   # Validates arguments
   arguments = [wikidata_id, property]
   for argument in arguments:
      if not argument:
         print(f'WikidataServices Error in get_property: empty {argument}')
         return None
   
   # Connection parameters
   wiki_api_url = 'https://www.wikidata.org/w/api.php'
   params = {
      'action': 'wbgetclaims',
      'format': 'json',
      'entity': wikidata_id,
      'property': property
   }
   
   # Sends requests with retry and exponential backoff mechanisms to avoid API saturation
   sleep_time = BASE_SLEEP
   
   for attempt in range(1, MAX_RETRIES + 1):
      try:
         
         # Requests Wikidata API
         res = requests.get(
            wiki_api_url, 
            params=params, 
            timeout=10
         )
         
         if res.status_code == 200: # OK
         
            data = res.json()
            
            # Empty response
            if not property in data.get('claims', {}): 
               print(f'WikidataServices Warning from get_property: Property {property} does not exist for wikidata id {wikidata_id}')   
               return None
            
            # Extracts property array
            return data['claims'][property]
         
         elif res.status_code == 429:  # too many requests
            retry_after = int(res.headers.get("Retry-After", sleep_time))
            if retry_after > MAX_ACCEPTABLE_WAIT:
               print(f"WikidataServices Error in get_wikidata_property: Retry-After is too long {retry_after} s.")
               return None
            else:
               print(f"WikidataServices Warning in get_wikidata_property: Too many requests. Waiting {sleep_time} seconds (backoff exponencial)...")
               time.sleep(sleep_time)
               sleep_time *= 2  # backoff exponencial

         else:
            print(f"WikidataServices Error in get_wikidata_property: HTTP {res.status_code} - {res.text}")
            break
         
      except HTTPError as e:
         print(f'WikidataServices Error in get_wikidata_property: HTTPError - {e}')
         time.sleep(sleep_time)
         sleep_time *= 2
      except RequestException as e:
         print(f'WikidataServices Error in get_wikidata_property: HTTP Request Error - {e}')
         time.sleep(sleep_time)
         sleep_time *= 2
      except Exception as e:
         print(f'WikidataServices Error in get_wikidata_property: {e}')
         time.sleep(sleep_time)
         sleep_time *= 2
   
   print(f'WikidataServices Error in get_wikidata_property: Failed after {MAX_RETRIES} attempts.')
   return None


def is_tennis_player(wikidata_id):
   """ Validates if the provided Wikidata entity is a tennis player.
   
   Args:
      wikidata_id (str): Wikidata entity ID to validate

   Returns:
      (bool or None): Validates if it a tennis player or None in case wikidata_id is empty
   """
   
   validated = False
   
   try:
      # Validates argument
      if not wikidata_id.strip():
         print('WikidataServices Error in is_tennis_player: empty wikidata_id.')
         return None
      
      # Requests Wikidata API for properties P106=job and P641=sport 
      jobs_claim = get_wikidata_property(wikidata_id, 'P106')
      sport_claim = get_wikidata_property(wikidata_id, 'P641')
      
      # Empty response
      if (not jobs_claim or len(jobs_claim) == 0) and (not sport_claim or len(sport_claim) == 0) :
         print(f'WikidataServices Warning from is_tennis_player: wikidata_id {wikidata_id} has not been validated as a tennis player. No properties P106, P641.')
         return False
      
      # Loops jobs claim array
      if (jobs_claim and len(jobs_claim) != 0):
         for job in jobs_claim:
            
            # Extracts job
            job_id = job['mainsnak']['datavalue']['value']['id']
            
            if job_id in ['Q10833314', 'Q11513337']:
               validated = True
               break
            
      # Loops sports claim array
      if (sport_claim and len(sport_claim) != 0):
         for sport in sport_claim:
            
            # Extracts sport
            sport_id = sport['mainsnak']['datavalue']['value']['id']
            
            if sport_id == 'Q847':
               validated = True
               break
         
      if validated:
         print(f'WikidataServices Info from is_tennis_player: wikidata_id {wikidata_id} has been validated as a tennis player.')
         return True
      else:
         print(f'WikidataServices Warning from is_tennis_player: wikidata_id {wikidata_id} has not been validated as a tennis player')
         return False
      
   except Exception as e:
      print(f'WikidataServices Error in is_tennis_player: {str(e)}')
      return False


def get_wikidata_id(name_last, name_first):
   """ Retrieves verified Wikidata ID for a tennis player searching by first and last name.

   Args:
      name_last (str): Player's last name.
      name_first (str): Player's first name.

   Returns:
      (str or None): verified Wikidata ID for a tennis player or None if not found
   """
     
   # Composes complete player name to search wikidata_id
   player_name = compose_name_for_search(name_last, name_first)

   # Validates argument
   if not player_name:
      print('WikidataServices Error in get_wikidata_id: empty player name.')
      return None

   # Connection parameters            
   wiki_api_url = f'https://www.wikidata.org/w/api.php'
   params = {
      'action': 'wbsearchentities',
      'format': 'json',
      'language': 'en',
      'search': player_name,
      'type': 'item',
      'limit': 1,
      'props': 'id'
   }

   # Sends requests with retry and exponential backoff mechanisms to avoid API saturation
   sleep_time = BASE_SLEEP
   
   for attempt in range(1, MAX_RETRIES + 1):
   
      try: 
         # Requests Wikidata API
         res = requests.get(
            wiki_api_url, 
            params=params, 
            timeout=10
         )
         
         if res.status_code == 200: # OK
         
            data = res.json()
            
            # Empty response
            if not data.get('search'):
               print(f'WikidataServices Warning from get_wikidata_id: No wikidata id has been found for player {player_name}')
               return None
            
            wikidata_id = data['search'][0]['id']
            
            # Empty response or not validated tennis player
            if not wikidata_id or not is_tennis_player(wikidata_id):
               print(f'WikidataServices Warning from get_wikidata_id: No wikidata id has been found for player {player_name}')
               return None
            
            # Validated wikidata_id found
            print(f'WikidataServices Info from get_wikidata_id: wikidata id {wikidata_id} has been found for player {player_name}')
            return wikidata_id
         
         elif res.status_code == 429:  # too many requests
            retry_after = int(res.headers.get("Retry-After", sleep_time))
            if retry_after > MAX_ACCEPTABLE_WAIT:
               print(f"WikidataServices Error in get_wikidata_id: Retry-After is too long {retry_after} s.")
               return None
            else:
               print(f"WikidataServices Warning: Too many requests. Waiting {sleep_time} seconds (backoff exponencial)...")
               time.sleep(sleep_time)
               sleep_time *= 2  # backoff exponencial

         else:
            print(f"WikidataServices Error: HTTP {res.status_code} - {res.text}")
            break
      
      except HTTPError as e:
         print(f'WikidataServices Error in get_wikidata_id: HTTPError - {e}')
         time.sleep(sleep_time)
         sleep_time *= 2
      except RequestException as e:
         print(f'WikidataServices Error in get_wikidata_id: HTTP Request Error - {e}')
         time.sleep(sleep_time)
         sleep_time *= 2
      except Exception as e:
         print(f'WikidataServices Error in get_wikidata_id: {e}')
         time.sleep(sleep_time)
         sleep_time *= 2
   print(f'WikidataServices Error in get_wikidata_id: Failed after {MAX_RETRIES} attempts.')
   return None


def get_wikidata_name_last(wikidata_id):
   """ Retrieves last name for the provided Wikidata ID.

   Args:
      wikidata_id (str): Wikidata entity ID

   Returns:
      (str or None): last name in Spanish or None if not found
   """
   
   try:
      # Validates argument 
      wikidata_id = wikidata_id.strip()
      if not wikidata_id:
         print('WikidataServices Error in get_wikidata_name_last: empty wikidata_id.')
         return None

      # Requests Wikidata API
      name_last_claim = get_wikidata_property(wikidata_id, 'P734')

      # Empty response
      if (not name_last_claim or len(name_last_claim) == 0):
         print(f'WikidataServices Warning from get_wikidata_name_last: No last name has been found for wikidata_id {wikidata_id}')
         return None
      
      # Extracts entity name_last ID
      name_last_id = name_last_claim[0]['mainsnak']['datavalue']['value']['id']
               
      # Requests label (text) for name_last ID in Spanish                 
      params_label = {
         'action': 'wbgetentities',
         'format': 'json',
         'ids': name_last_id,
         'props': 'labels',
         'languages': 'es'
      }
      res = requests.get(wiki_api_url, params=params_label, timeout=10)
      data = res.json()
      name_last = data['entities'][name_last_id]['labels']['es']['value']
      
      # Empty
      if not name_last:
         print(f'WikidataServices Warning from get_wikidata_name_last: No last name has been found for wikidata_id {wikidata_id}')
         return None
   
      print(f'WikidataServices: last name {name_last} has been found for wikidata id {wikidata_id}')
      return name_last
      
   except Exception as e:
      print(f'WikidataServices Error in get_wikidata_name_last: {str(e)}')
      return None


def get_wikidata_name_first(wikidata_id):
   """ Retrieves first name for the provided Wikidata ID.

   Args:
      wikidata_id (str): Wikidata entity ID

   Returns:
      (str or None): first name in Spanish or None if not found
   """
   
   try:
      # Validates argument 
      wikidata_id = wikidata_id.strip()
      if not wikidata_id:
         print('WikidataServices Error in get_wikidata_name_first: empty wikidata_id.')
         return None

      # Requests Wikidata API
      name_first_claim = get_wikidata_property(wikidata_id, 'P735')

      # Empty response
      if (not name_first_claim or len(name_first_claim) == 0):
         print(f'WikidataServices Warning from get_wikidata_name_first: No last name has been found for wikidata_id {wikidata_id}')
         return None
      
      # Extracts entity name_first ID
      name_first_id = name_first_claim[0]['mainsnak']['datavalue']['value']['id']
               
      # Requests label for name_first ID            
      params_label = {
         'action': 'wbgetentities',
         'format': 'json',
         'ids': name_first_id,
         'props': 'labels',
         'languages': 'es'
      }
      res = requests.get(wiki_api_url, params=params_label, timeout=10)
      data = res.json()
      name_first = data['entities'][name_first_id]['labels']['es']['value']
      
      # Empty
      if not name_first:
         print(f'WikidataServices Warning from get_wikidata_name_first: No last name has been found for wikidata_id {wikidata_id}')
         return None
   
      print(f'WikidataServices: last name {name_first} has been found for wikidata id {wikidata_id}')
      return name_first
      
   except Exception as e:
      print(f'WikidataServices Error in get_wikidata_name_first: {str(e)}')
      return None


def get_wikidata_country(wikidata_id):
   """ Retrieves ISO-3166-1 alpha-2 country code for provided Wikidata entity ID.

   Args:
      wikidata_id (str): Wikidata entity ID.

   Returns:
      (str or None): ISO-3166-1 alpha-2 country code in lowercase, or None if not found.
   """

   try:

      # Validates argument
      wikidata_id = wikidata_id.strip()
      if not wikidata_id:
         print('WikidataServices Error in get_wikidata_country: empty wikidata_id.')
         return None

      # Requests the country (P27 property) to Wikidata API
      country_claim = get_wikidata_property(wikidata_id, 'P27')

      # Empty response
      if (not country_claim or len(country_claim) == 0):
         print(f'WikidataServices Warning from get_wikidata_country: No country id has been found for wikidata_id {wikidata_id}')
         return None
      
      # Extracts entity country ID
      country_id = country_claim[0]['mainsnak']['datavalue']['value']['id']
      
      # Empty response
      if not country_id:
         print(f'WikidataServices Warning from get_wikidata_country: No country id has been found for wikidata_id {wikidata_id}')
         return None
      
      # Requests Wikidata API for country ISO-3166-1 alpha-2
      alpha2_claim = get_wikidata_property(country_id, 'P297')
      
      # Empty response
      if not alpha2_claim or len(alpha2_claim) == 0:
         print(f'WikidataServices Warning from get_wikidata_country: No alpha2 code has been found for country_id {country_id}')
         return None
         
      # Extracts alpha2   
      country_alpha2 = alpha2_claim[0]["mainsnak"]["datavalue"]["value"] 
      
      # Empty response
      if not country_alpha2:
         print(f'WikidataServices Warning from get_wikidata_country: No alpha2 code has been found for wikidata id {wikidata_id} country id {country_id}')
         return None
      
      # Country found      
      print(f'WikidataServices Info from get_wikidata_country: alpha2 code has been found for wikidata id {wikidata_id} country id {country_id}')
      return country_alpha2.lower()

   except Exception as e:
      print(f'WikidataServices Error in get_wikidata_country: {str(e)}')
      return None
   

def get_wikidata_birth_date(wikidata_id):
   """ Retrieves and formats birth date for provided Wikidata entity ID.

   Args:
      wikidata_id (str): Wikidata entity ID to search for the birth date.

   Returns:
      (str or None): birth date with format "DD-MM-YYYY", or None if not found.
   """

   try:
      # Validates argument
      wikidata_id = wikidata_id.strip()
      if not wikidata_id:
         print( 'WikidataServices Error in get_wikidata_birth_date: empty wikidata_id.')
         return None

      # Requests Wikidata API
      birth_date_claim = get_wikidata_property(wikidata_id, 'P569')

      # Empty response
      if (not birth_date_claim or len(birth_date_claim) == 0):
         print(f'WikidataServices Warning from get_wikidata_birth_date: No birth_date has been found for wikidata_id {wikidata_id}')
         return None
      
      # Extracts birth date
      birth_date = birth_date_claim[0]['mainsnak']['datavalue']['value']['time']
      
      # Empty response
      if not birth_date:
         print(f'WikidataServices Warning from get_wikidata_birth_date: No birth_date has been found for wikidata_id {wikidata_id}')
         return None

      # Formats birth date found into frontend format
      frontend_format="%d-%m-%Y"

      if birth_date.startswith("+"):
         birth_date = birth_date[1:]
         
      if "T" in birth_date and "Z" in birth_date:   # 2007-10-01T00:00:00Z
         birth_date_obj = datetime.fromisoformat(birth_date.replace("Z", "+00:00"))
    
      elif "T" in birth_date:                         # 2007-10-01T00:00:00
         birth_date_obj = datetime.fromisoformat(birth_date)
    
      elif birth_date.count("-") == 2:                # 2007-10-01
         birth_date_obj = datetime.fromisoformat(birth_date)
      
      elif birth_date.count("-") == 1:                # 2007-10
         birth_date_obj = datetime.fromisoformat(birth_date + "-01")

      else:                                              # 2007
         birth_date_obj = datetime.fromisoformat(birth_date + "-01-01")
    
      formatted_birth_date = birth_date_obj.strftime(frontend_format)
    
      print(f'WikidataServices Info from get_wikidata_birth_date: birth date {formatted_birth_date} has been found for wikidata id {wikidata_id}')
      return formatted_birth_date
            
   except Exception as e:
      print(f'WikidataServices Error in get_wikidata_birth_date: {str(e)}')
      return None
   

def get_wikidata_height(wikidata_id):
   """ Retrieves and normalizes the height in cm for provided Wikidata entity ID.

   Args:
      wikidata_id (str): Wikidata entity ID.

   Returns:
      (str or None): Height in centimeters or None if not found.
   """

   try:
      # Validates argument 
      wikidata_id = wikidata_id.strip()
      if not wikidata_id:
         print('WikidataServices Error in get_wikidata_height: empty wikidata_id.')
         return None

      # Requests Wikidata API
      height_claim = get_wikidata_property(wikidata_id, 'P2048')

      # Empty response
      if (not height_claim or len(height_claim) == 0):
         print(f'WikidataServices Warning from get_wikidata_height: No height has been found for wikidata_id {wikidata_id}')
         return None
      
      # Extracts height value and unit
      height = height_claim[0]['mainsnak']['datavalue']['value']['amount'] # +1.85
      unit = height_claim[0]['mainsnak']['datavalue']['value']['unit'] #http://www.wikidata.org/entity/Q11573
      
      # Empty response
      if (not height or not unit):
         print(f'WikidataServices Warning from get_wikidata_height: No height has been found for wikidata_id {wikidata_id}')
         return None      
      
      # Conversion to cm 
      units_dict = {
         'Q11573': 100,    # m
         'Q174728': 1,     # cm
         'Q3710': 30.48,   # feet
         'Q218593': 2.54,  # inches
      }

      # Clean value and unit
      clean_height = float(height.lstrip('+'))
      clean_unit = unit.split('/')[-1]
            
      # Unknown units      
      if clean_unit not in units_dict:
         print(f'WikidataServices Warning from get_wikidata_height: No height has been found for wikidata_id {wikidata_id}')
         return None
      
      # Converts to cm
      height_in_cm = str(int( clean_height * units_dict[clean_unit]))
   
      print(f'WikidataServices Info from get_wikidata_height: height {height_in_cm} cm has been found for wikidata id {wikidata_id}')
      return height_in_cm
      
   except Exception as e:
      print(f'WikidataServices Error in get_wikidata_height: {str(e)}')
      return None
   

def get_wikidata_weight(wikidata_id):
   """ Retrieves and normalizes the weight in kg for provided Wikidata entity ID.

   Args:
      wikidata_id (str): Wikidata entity ID.

   Returns:
      (str or None): Weight in kilograms or None if not found.
   """
   try:
      # Validates argument
      wikidata_id = wikidata_id.strip()
      if not wikidata_id:
         print('WikidataServices Error in get_wikidata_weight: empty wikidata_id.')
         return None

      # Requests Wikidata API
      weight_claim = get_wikidata_property(wikidata_id, 'P2067')

      # Empty response
      if (not weight_claim or len(weight_claim) == 0):
         print(f'WikidataServices Warning from get_wikidata_weight: No weight has been found for wikidata_id {wikidata_id}')
         return None
      
      # Extracts weight value and unit
      weight = weight_claim[0]['mainsnak']['datavalue']['value']['amount'] # +80
      unit = weight_claim[0]['mainsnak']['datavalue']['value']['unit'] # http://www.wikidata.org/entity/Q11570
      
      # Empty response
      if (not weight or not unit):
         print(f'WikidataServices Warning from get_wikidata_weight: No weight has been found for wikidata_id {wikidata_id}')
         return None    
      
      # Conversion to kg
      units_dict = {
         'Q11570': 1,      # kg
         'Q19908': 0.4536, # lbs to kg
      }

      # Clean value and unit
      clean_weight = float(weight.lstrip('+'))
      clean_unit = unit.split('/')[-1]
      
      # Unknown units  
      if clean_unit not in units_dict:
         print(f'WikidataServices Warning from get_wikidata_weight: No weight has been found for wikidata_id {wikidata_id}')
         return None
      
      # Converts to kg
      weight_in_kg = str(int(clean_weight * units_dict[clean_unit]))
         
      print(f'WikidataServices Info from get_wikidata_weigth: weight {weight_in_kg} kg has been found for wikidata id {wikidata_id}')
      return weight_in_kg
      
   except Exception as e:
      print(f'WikidataServices Error in get_wikidata_weight: {str(e)}')
      return None
   
   
def get_wikidata_hand(wikidata_id):
   """
   Retrieves the handedness of a player for provided Wikidata entity ID.

   Args:
      wikidata_id (str): Wikidata entity ID.

   Returns:
      (str or None): "Derecha" for right-handed players, "Izquierda" for left-handed players, or None if not found.
   """

   try:
      # Validates argument 
      wikidata_id = wikidata_id.strip()
      if not wikidata_id:
         print('WikidataServices Error in get_wikidata_hand: empty wikidata_id.')
         return None
      
      # Requests Wikidata API
      hand_claim = get_wikidata_property(wikidata_id, 'P552')

      # Empty response
      if (not hand_claim or len(hand_claim) == 0):
         print(f'WikidataServices Warning from get_wikidata_hand: No hand has been found for wikidata_id {wikidata_id}')
         return None
      
      # Extracts entinty hand id
      hand = hand_claim[0]['mainsnak']['datavalue']['value']['id']
      
      hand_dict = {
         'Q1310443': 'Derecha',
         'Q3029952': 'Izquierda',
      }
      
      # Empty or unknown hand
      if (not hand or (not hand in hand_dict)):
         print(f'WikidataServices Warning from get_wikidata_hand: No hand has been found for wikidata_id {wikidata_id}')
         return None
      
      # Format hand   
      formatted_hand = hand_dict[hand]
               
      print(f'WikidataServices: hand {formatted_hand} has been found for wikidata id {wikidata_id}')
      return formatted_hand
      
   except Exception as e:
      print(f'WikidataServices Error in get_wikidata_hand: {str(e)}')
      return None
   
   
def get_wikidata_networks(wikidata_id, network='instagram'):
   """ Retrieves network username for a provided Wikidata entity ID and composes network link.
   
   Args:
      wikidata_id (str): 
      network (str): network name. Allowed networks: instagram, facebook, x_twitter.
   
   Returns:
      (str or None): network link.
   """
   
   try:
      
      # Wikidata properties for networks
      networks_data = {
         'instagram': {
            'prop':'P2003',
            'url': 'https://www.instagram.com/'
         },
         'facebook': {
            'prop': 'P2013',
            'url': 'https://www.facebook.com/'
         },
         'x_twitter': {
            'prop': 'P2002',
            'url': 'https://x.com/'
         }
      }
      
      # Validates arguments
      if not wikidata_id.strip():
         print('WikidataServices Error in get_wikidata_networks: empty wikidata_id.')
         return None
      elif network not in networks_data:
         print('WikidataServices Error in get_wikidata_networks: unknown network provided.')
         return None

      # Requests Wikidata API
      username_claim = get_wikidata_property(wikidata_id, networks_data[network]['prop'])

      # Empty response
      if not username_claim or len(username_claim) == 0:
         print(f'WikidataServices Warning from get_wikidata_networks: No {network} username has been found for wikidata_id {wikidata_id}.')
         return None
         
      else:
         # Extracts username
         username = username_claim[0]['mainsnak']['datavalue']['value']
         
         # Empty response
         if not username:
            print(f'WikidataServices Warning from get_wikidata_networks: No {network} username has been found for wikidata_id {wikidata_id}')
            return None
            
         else:
            # Composes URL
            #return f'{networks_data[network]['url']}{username}'
            # Returns username
            return f'{username}'

   except Exception as e:
      print(f'WikidataServices Error in get_wikidata_networks: {str(e)}')
      return None
   
   
def get_wikidata_pro_since(wikidata_id):
   """ Retrieves the year when a player turned professional for the provided Wikidata entity ID.

   Args:
      wikidata_id (str): Wikidata entity ID.

   Returns:
      (str or None): Year when the player turned professional with format 4-digit string, or None if not found.
   """

   try:
      # Validates argument 
      wikidata_id = wikidata_id.strip()
      if not wikidata_id:
         print('WikidataServices Error in get_wikidata_pro_since: empty wikidata_id.')
         return None

      # Requests Wikidata API
      pro_since_claim = get_wikidata_property(wikidata_id, 'P2031')

      # Empty response
      if (not pro_since_claim or len(pro_since_claim) == 0):
         print(f'WikidataServices Warning in get_wikidata_pro_since: No pro_since year found for wikidata_id {wikidata_id}')
         return None

      # Extracts pro_since date
      pro_since = pro_since_claim[0]['mainsnak']['datavalue']['value']['time']
      
      # Empty response      
      if not pro_since:
         print(f'WikidataServices Warning in get_wikidata_pro_since: No pro_since year found for wikidata_id {wikidata_id}')
         return None

      # Extracts year  +2005-04-30T00:00:00Z
      if pro_since.startswith("+"):
         pro_since = pro_since[1:]
      pro_since_year = str(int(pro_since[0:4]))
      
      print(f'WikidataServices Info from get_wikidata_pro_since: Professional since {pro_since_year} has been found for wikidata id {wikidata_id}')

      return pro_since_year

   except Exception as e:
      print(f'WikidataServices Error in get_wikidata_pro_since: {str(e)}')
      return None
   

def compose_name_for_search(name_last, name_first='-'):
   """ Composes a complete player name to search its wikidata ID.

   Args:
      name_last (str): Player's last name.
      name_first (str): Player's first name.

   Returns:
      (str or None): Full name or None if last name is invalid.
   """
   
   name_last = name_last.strip()
   name_first = name_first.strip()
   
   if name_last is None:
      return None

   # If first name is not valid, only uses last name
   return name_last if (name_first == '-' or name_first == 'unknown') else name_first + ' ' + name_last
      
      
def get_wikidata_enrichment(player):
   """ Searches in Wikidata the missing fields of the provided player.
   
   Args:
      player (dict): register from database
   
   Return:
      (boolean): if player_object must be commited into the database (if enriched)
      (dict): enriched player or player
   """ 
   
   update_flag = False
   
   wikidata_id = player['wikidata_id']
   
   # Gets wikidata id if missing
   if (wikidata_id is None or
       wikidata_id == '-' or
       wikidata_id == 'unknown'):
         
      wikidata_id = get_wikidata_id(player['name_last'], player['name_first'])
      
      if (wikidata_id and player['wikidata_id'] != wikidata_id):
         player['wikidata_id'] = wikidata_id
         update_flag = True
      else:
         # Wikidata id has not been found. No enrichment
         return update_flag, player
   
   
   # Fields to enrich if missing
   fields = list(player.keys())
   exclude_fields = ['player_id', 'wikidata_id', 'fullname']
   for f in exclude_fields:
      if f in fields:
         fields.remove(f)
   
   networks_fields = ['instagram', 'facebook', 'x_twitter']
      
   for field in fields:
      # if missing
      if (player[field] is None or 
          player[field] == '-' or 
          player[field] == 'unknown' or 
          (field == 'birth_date' and player['birth_date'] == '01-01-1800')):
         
         function_name = 'get_wikidata_networks' if field in networks_fields else f'get_wikidata_{field}'
         
         function = globals().get(function_name)
         if function:
            
            # Wikidata enrichment
            enriched_value = function(wikidata_id, field) if field in networks_fields else function(wikidata_id)
            
            if (enriched_value and player[field] != enriched_value):
               player[field] = enriched_value
               update_flag = True
         else:
            print(f'WikidataServices Warning in get_wikidata_enrichment: Function {function_name} not found')
               
   return update_flag, player