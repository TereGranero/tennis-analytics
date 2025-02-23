<template>
      <div class="row d-flex flex-wrap gap-3 justify-content-center">

         <!-- Player photo -->
         <div class="col-md-4 d-flex justify-content-center align-items-center">
            <img 
               v-if="urlPlayerImage" 
               :src="urlPlayerImage" 
               :alt="urlPlayerImage" 
               width="250" />
            <span v-else class="text-center"> Imagen no disponible</span>
         </div>  

         <!-- Personal details -->
         <div class="col-md-7">
            <h3 class="mb-3">DETALLES PERSONALES</h3>
            <table class="table table-hover">
               <tbody>
                  <tr v-if="player.country !== 'unknown' && player.country !== '-'">
                     <th scope="row">País:</th>
                     <td> {{ countryName }}</td>
                  </tr>
                  <tr>
                     <th scope="row">Nacimiento:</th>
                     <td>{{ player.birth_date }}</td>
                  </tr>
                  <tr>
                     <th scope="row">Mano:</th>
                     <td>{{ player.hand }}</td>
                  </tr>
                  <tr>
                     <th scope="row">Altura en cm:</th>
                     <td>{{ player.height }}</td>
                  </tr>
                  <tr>
                     <th scope="row">Peso en kg:</th>
                     <td> {{ player.weight }} </td>
                  </tr>
                  <tr>
                     <th scope="row">Profesional desde: </th>
                     <td> {{ player.pro_since }} </td>
                  </tr>
                  <tr>
                     <th scope="row">Síguelo en:</th>
                     <td>  
                        <i 
                           v-if="player.instagram !== '-'"
                           class="fa-brands fa-instagram text-secondary cursor-pointer me-2"
                           @click="goToNetwork('instagram', player.instagram)">
                        </i>
                        <i 
                           v-if="player.facebook !== '-'"
                           class="fa-brands fa-facebook text-secondary cursor-pointer me-2"
                           @click="goToNetwork('facebook', player.facebook)">
                        </i>

                        <i 
                           v-if="player.x_twitter !== '-'"
                           class="fa-brands fa-x-twitter text-secondary cursor-pointer"
                           @click="goToNetwork('twitter', player.x_twitter)">
                        </i>
                     </td>
                  </tr>
               </tbody>
            </table>
         </div>
      </div>
</template>

<script>
import countries from 'i18n-iso-countries'
import es from 'i18n-iso-countries/langs/es.json'
import { getWikiPlayerImage } from '@/api/connectionService'

export default {
   props: {
      player: Object,
   },

   data() {
      return {
         urlPlayerImage: null,
         countryName: null,
      }
   },
   
   watch: {
      // Loads when data is available
      
      'player.wikidata_id': {
         immediate: true, // If value is not null, launches
         handler(newWikidata_id) {
            if (newWikidata_id && newWikidata_id !== '-') {
               this.getPlayerImage();
            }
         }
      },

      'player.country': {
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
            this.countryName = countries.getName(this.player.country.toUpperCase(), 'es')      
         } catch (err) {
            console.error(`Error retrieving country name from i18n-iso-countries: ${err}`)
         }
      },
      
      async getPlayerImage() {
         try{
            this.urlPlayerImage = await getWikiPlayerImage(this.player.wikidata_id)
         } catch (err) {
            console.error(`Error retrieving Wikidata player image: ${err}`)
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

<style scoped>
   img {
      border: 1px solid #140202;
   }
</style>