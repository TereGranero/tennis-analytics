def validate_request_data(data, method):
   keys = [
      'player_id',
      'name_first',
      'name_last',
      'hand',
      'birth_date',
      'country',
      'height',
      'wikidata_id',
      'fullname',
      'weight',
      'instagram',
      'facebook',
      'x_twitter',
      'pro_since'
   ]
   
   for key in keys:
      if key not in data:
         return False
   
   name_last = data.get('name_last', 0 )
   
   if (method =='POST'):
      
      player_id = data.get('player_id', 0 )

      return False if not ( isinstance(player_id, str) and
         isinstance(name_last, str) and
         len(player_id) > 2 and
         len(name_last) > 1 ) else True
      
   elif (method =='PUT'):
      return False if not( isinstance(name_last, str) and
            len(name_last) > 1 ) else True
      