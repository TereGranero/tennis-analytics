<template>
   <div class="d-flex flex-row flex-wrap gap-5 justify-content-center align-items-center mb-5">

      <!-- Player photo -->
      <figure 
         v-if="urlPlayerImage" 
         class="d-flex flex-column align-items-center text-center">
         <img 
            :src="urlPlayerImage"
            class="img-fluid photo" 
            :alt="imageAttribution.description" />

         <!-- Attribution -->
         <figcaption 
            v-if="imageAttribution" 
            class="mt-2 text-muted text-break">
            <small>
               "<span v-html="imageAttribution.title"></span>" por <span v-html="imageAttribution.author"></span>,
               bajo licencia <a :href="imageAttribution.licenseUrl" target="_blank">{{ imageAttribution.license }}</a>.
               <a :href="imageAttribution.filePageUrl" target="_blank">Ver en Wikimedia Commons</a>
            </small>
         </figcaption>
      </figure>   

      <!-- Personal details -->
      <div class="d-flex flex-column align items-start">
         <h2 class="text-responsive-3 fw-bold m-0">
            DETALLES PERSONALES
         </h2>
         <table class="table table-hover mt-3">
            <tbody>
               <tr 
                  v-if="player.country !== 'unknown' && player.country !== '-'"
                  class="text-responsive-4">
                  <th scope="row">País:</th>
                  <td class="text-center"> {{ countryName }}</td>
               </tr>
               <tr class="text-responsive-4">
                  <th scope="row">Nacimiento:</th>
                  <td class="text-center">{{ player.birth_date }}</td>
               </tr>
               <tr class="text-responsive-4">
                  <th scope="row">Mano:</th>
                  <td class="text-center">{{ player.hand }}</td>
               </tr>
               <tr class="text-responsive-4">
                  <th scope="row">Altura en cm:</th>
                  <td class="text-center">{{ player.height }}</td>
               </tr>
               <tr class="text-responsive-4">
                  <th scope="row">Peso en kg:</th>
                  <td class="text-center"> {{ player.weight }} </td>
               </tr>
               <tr class="text-responsive-4">
                  <th scope="row">Profesional desde: </th>
                  <td class="text-center"> {{ player.pro_since }} </td>
               </tr>
               <tr class="text-responsive-4">
                  <th scope="row">Síguelo en:</th>
                  <td class="text-center">  
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
import { getWikiDataImage } from '@/api/wikiDataConnectionService.js'

export default {
   
   name: 'PlayerBio',

   props: {
      player: {
         type: Object,
         required: true
      }
   },

   data() {
      return {
         urlPlayerImage: null,
         imageAttribution: null,
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
            const res = await getWikiDataImage(this.player.wikidata_id)
            if (res){
               this.urlPlayerImage = res.imageUrl
               this.imageAttribution = res.imageAttribution
            }

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

figure {
   max-width: 300px;
}

.photo {
   width: auto;
   max-height: 350px;
   border: 1px solid #576973;
}
</style>