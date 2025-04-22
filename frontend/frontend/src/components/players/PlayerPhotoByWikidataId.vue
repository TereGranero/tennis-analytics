<template>

   <!-- Player photo -->
   <figure 
      v-if="urlPlayerImage" 
      class="d-flex flex-column align-items-center text-center">
      <img 
         :src="urlPlayerImage"
         :alt="imageAttribution.description"
         class="img-fluid photo"
         :class="{ 'fixed-height': setHeight }" />

      <!-- Attribution -->
      <figcaption 
         v-if="imageAttribution" 
         class="mt-2 text-muted text-break">
         <small>
            "<span v-html="imageAttribution.title" class="fw-bold"></span>" por <span v-html="imageAttribution.author"></span>,
            licencia <a 
               :href="imageAttribution.licenseUrl" 
               target="_blank"
               :aria-label="`Ver licencia ${imageAttribution.license} (se abre en nueva ventana)`">
               {{ imageAttribution.license }}
            </a>.
            <a 
               :href="imageAttribution.filePageUrl" 
               target="_blank"
               aria-label="Ver imagen original en Wikimedia Commons (se abre en nueva ventana)"> 
               Ver Wikimedia Commons
            </a>
         </small>
      </figcaption>
   </figure>   

</template>

<script>
import { getWikiDataImage } from '@/api/wikiDataConnectionService.js'

export default {
   
   name: 'PlayerPhotoByWikidataId',

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