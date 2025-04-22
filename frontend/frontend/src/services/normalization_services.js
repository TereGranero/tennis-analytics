export const normalizeIntoBackend = (player) => {
   for (const [field, value] of Object.entries(player)) {

      if ([
         'height', 
         'weight',
         'pro_since'
      ].includes(field)) {
         player[field] =  (value === '' || value == 0) ? '-' : value.toString()
      }

      if (([
         'name_first', 
         'name_last', 
         'hand',
         'country',
         'wikidata_id', 
         'instagram', 
         'facebook', 
         'x_twitter'
      ].includes(field)) && (value === '')){
         player[field] = '-'
      }

      if (field === 'birth_date') {
         if (!value) { 
            player[field] = '1800-01-01'
         }
      }
   }
   return player
};


export const normalizeIntoForm = (player) => {

   // Capitalizes country
   if (player.country) {
      player.country = (player.country == 'unknown') ? '-' : player.country.toUpperCase()
   } else {
      player.country = '-'
   }

   // Formats birth date dd-mm-yyyy --> yyyy-mm-dd
   if (player.birth_date) {
      const [day, month, year] = player.birth_date.split('-')
      player.birth_date = `${year}-${month}-${day}`
   }

   // Convert to numbers
   try {
      if (player.height) {
         player.height = (player.height == '-') ? 0 : parseInt(player.height, 10)
      } else {
         player.height = 0
      }
   }catch(err){
      console.error(`Converting height Error: ${err}`)
      player.height = 0
   }

   try {
      if (player.weight) {
         player.weight = (player.weight == '-') ? 0 : parseInt(player.weight, 10)
      } else {
         player.weight = 0
      }
   }catch(err){
      console.error(`Converting weight Error: ${err}`)
      player.weight = 0
   }

   try {
      if (player.pro_since) {
         player.pro_since = (player.pro_since == '-') ? 0 : parseInt(player.pro_since, 10)
      } else {
         player.pro_since = 0
      }
   }catch(err){
      console.error(`Converting pro_since year Error: ${err}`)
      player.pro_since = 0
   }

   return player
};

export const convertIntoSlug = (name) => {
   return name.toLowerCase().replace(/\s+/g, '-')
};
