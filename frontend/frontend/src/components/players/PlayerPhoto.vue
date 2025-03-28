<template>

   <!-- Player photo -->
   <figure 
      v-if="urlPlayerImage" 
      class="d-flex flex-column align-items-center text-center">
      <img 
         :src="urlPlayerImage"
         class="img-fluid photo"
         :class="{ 'fixed-height': setHeight }"
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

</template>

<script>
import { getWikiDataImage } from '@/api/wikiDataConnectionService.js'

export default {
   
   name: 'PlayerPhoto',

   props: {
      playerWikidataId: {
         type: String,
         required: true
      },

      setHeight: {
         type: Boolean,
         default: false
      }
   },

   data() {
      return {
         urlPlayerImage: null,
         imageAttribution: null,
      }
   },

   methods: {
      async getPlayerImage() {
         try{
            const res = await getWikiDataImage(this.playerWikidataId)
            if (res){
               this.urlPlayerImage = res.imageUrl
               this.imageAttribution = res.imageAttribution
            }

         } catch (err) {
            console.error(`Error retrieving Wikidata player image: ${err}`)
         }
      }
   },

   async mounted() {
      await this.getPlayerImage()
   }

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

   .fixed-height {
      height: 300px;
      width: auto;
      max-width: 100%;
      object-fit: contain;
      border: none;
   }

</style>