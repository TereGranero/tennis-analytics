<template>
   <tr>
      <!-- Full Name -->
      <td 
         @click="$emit('view-player', playerRow.player_id)" 
         class="cursor-pointer">
         {{ playerRow.fullname }}
      </td>

      <!-- Flag and country -->
      <td> 
         <img
            v-if="playerRow.country !== 'unknown'"
            :src="'https://flagcdn.com/w40/' + playerRow.country + '.png'"
            :alt="playerRow.country"
            :title="playerRow.country"
            class="flag me-2"> 
         <span v-if="playerRow.country !== 'unknown' && playerRow.country !== '-'"> 
            {{ countryName }}
         </span>
      </td>

      <!-- Birthday -->
      <td>{{ playerRow.birth_date }}</td>

      <!-- Font Awesome Buttons -->
      <td v-if="isAdmin">
         <i class="fas fa-eye text-secondary cursor-pointer me-2" 
            @click="$emit('view-player', playerRow.player_id)" 
            title="Ver"></i>
         <i class="fas fa-edit text-secondary cursor-pointer me-2" 
            @click="$emit('edit-player', playerRow.player_id)" 
            title="Editar"></i>
         <i class="fas fa-trash text-secondary cursor-pointer" 
            @click="$emit('delete-player', playerRow.player_id)" 
            title="Borrar"></i>
      </td>
   </tr>
</template>

<script>
import countries from 'i18n-iso-countries'
import es from 'i18n-iso-countries/langs/es.json'

export default {

   name: 'PlayerItem',

   props: {
      playerRow: {
         type: Object,
         required: true
      },
      isAdmin: {
         type: Boolean,
         required: true
      }

   },

   data() {
      return {
         countryName: null,
      }
   },

   watch: {
      // Loads when data is available
      'playerRow.country': {
         immediate: true, 
         handler(newCountry) {
            if (newCountry && newCountry !== '-' && newCountry !== 'unknown') {
               this.initCountry();
            }
         }
      }
   },

   methods: {
      initCountry() {
         try {
            countries.registerLocale(es)
            this.countryName = countries.getName(this.playerRow.country.toUpperCase(), 'es')      
         } catch (err) {
            console.error(`Error retrieving country name from i18n-iso-countries: ${err}`)
         }
      },
   }
}
</script>

<style> </style>
