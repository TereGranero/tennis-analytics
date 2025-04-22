<template>
   <section
      v-if="player"
      class="d-flex flex-row flex-wrap gap-5 justify-content-center align-items-center mb-5"
      aria-labelledby="bioTitle">

      <!-- Player photo -->
      <PlayerPhotoByWikidataId
         :playerWikidataId="player.wikidata_id"/>   

      <!-- Personal details -->
      <div class="d-flex flex-column align items-start">
         <h2 
            id="bioTitle"
            class="text-responsive-3 fw-bold m-0">
            DETALLES PERSONALES
         </h2>
         <table class="table table-hover mt-3">
            <caption class="visually-hidden">
               Detalles personales del jugador {{ player.fullname }}.
            </caption>
            <tbody>
               <tr 
                  v-if="player.country !== 'unknown' && player.country !== '-'"
                  class="text-responsive-4">
                  <th 
                     scope="row"
                     id="countryLabel">
                     País:
                  </th>
                  <td 
                     aria-labelledby="countryLabel"
                     class="text-center text-green"> 
                     {{ countryName }}
                  </td>
               </tr>

               <tr class="text-responsive-4">
                  <th 
                     scope="row"
                     id="birthLable">
                     Nacimiento:
                  </th>
                  <td
                     aria-labelledby="birthLabel"
                     class="text-center text-green">
                     {{ player.birth_date }}
                  </td>
               </tr>

               <tr 
                  class="text-responsive-4">
                  <th 
                     scope="row"
                     id="handLabel">
                     Mano:
                  </th>
                  <td
                     aria-labelledby="handLabel"
                     class="text-center text-green">
                     {{ player.hand }}
                  </td>
               </tr>

               <tr class="text-responsive-4">
                  <th 
                     scope="row"
                     id="heightLabel">
                     Altura en cm:
                  </th>
                  <td 
                     class="text-center text-green"
                     aria-labelledby="handLabel">
                     {{ player.height }}
                  </td>
               </tr>

               <tr class="text-responsive-4">
                  <th 
                     scope="row"
                     id="weightLabel">
                     Peso en kg:
                  </th>
                  <td 
                     class="text-center text-green"
                     aria-labelledby="weightLabel"> 
                     {{ player.weight }} 
                  </td>
               </tr>

               <tr class="text-responsive-4">
                  <th 
                     scope="row"
                     id="proSinceLabel">
                     Profesional desde: 
                  </th>
                  <td 
                     class="text-center text-green"
                     aria-labelledby="proSinceLabel"> 
                     {{ player.pro_since }} 
                  </td>
               </tr>

               <tr class="text-responsive-4">
                  <th 
                     scope="row"
                     id="mediaLabel">
                     Síguelo en:
                  </th>
                  <td 
                     class="text-center text-green"
                     aria-labelledby="mediaLabel">  
                     <button 
                        v-if="player.instagram !== '-'"
                        class="btn btn-link p-0 cursor-pointer"
                        @click="goToNetwork('instagram', player.instagram)"
                        :aria-label="`Ir al Instagram de ${ player.fullname }`">
                        <i class="fa-brands fa-instagram me-2 text-green"></i>
                     </button>
                     <button 
                        v-if="player.facebook !== '-'"
                        class="btn btn-link p-0 cursor-pointer"
                        @click="goToNetwork('facebook', player.facebook)"
                        :aria-label="`Ir al Facebook de ${ player.fullname }`">
                        <i class="fa-brands fa-facebook me-2 text-green"></i>
                     </button>
                     <button 
                        v-if="player.x_twitter !== '-'"
                        class="btn btn-link p-0 cursor-pointer"
                        @click="goToNetwork('twitter', player.x_twitter)"
                        :aria-label="`Ir al Twitter de ${ player.fullname }`">
                        <i class="fa-brands fa-x-twitter text-green"></i>
                     </button>
                  </td>
               </tr>
            </tbody>
         </table>
      </div>
   </section>
</template>

<script>
import countries from 'i18n-iso-countries'
import es from 'i18n-iso-countries/langs/es.json'
import PlayerPhotoByWikidataId from './PlayerPhotoByWikidataId.vue'

export default {
   
   name: 'PlayerBio',

   components: { PlayerPhotoByWikidataId },

   props: {
      player: {
         type: Object,
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
      'player.country': {
         immediate: true, 
         handler(newCountry) {
            if (newCountry && newCountry !== '-' && newCountry !== 'unknown') {
               this.initCountry()
            }
         }
      }
   },

   methods: {
      initCountry() {
         try {
            countries.registerLocale(es)
            this.countryName = countries.getName(this.player.country.toUpperCase(), 'es')      
         } catch (err) {
            console.error(`Error retrieving country name from i18n-iso-countries: ${err}`)
         }
      },

      goToNetwork(network, username) {
         const url_list = {
            instagram: `https://www.instagram.com/${username}`,
            facebook: `https://www.facebook.com/${username}`,
            twitter: `https://x.com/${username}`
         };

         if (url_list[network]) {
            window.open(url_list[network], '_blank');
         }
      }
   },

   async mounted() {
      this.initCountry()
   },

}
</script>

<style></style>