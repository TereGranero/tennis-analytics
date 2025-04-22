<template>
   <div>
      <!-- Player Photo -->
      <figure 
         v-if="urlImage"  
         class="text-center">
         <img
            :src="urlImage" 
            :alt="`Foto de ${alt}`"
            class="img-fluid photo" 
            :class="{ 'fixed-height': setHeight }"/>
         
         <!-- Attribution -->
         <figcaption 
            v-if="imageAttribution"
            class="mt-2 text-muted text-break ">
            <span class="fw-bold">{{ msg }} </span><br>
            <small>
               "<span v-html="imageAttribution.title"></span>" por <span v-html="imageAttribution.author"></span>,
               licencia <a 
                  :href="imageAttribution.licenseUrl"
                  target="_blank"
                  :aria-label="`Ver licencia ${ imageAttribution.license } (se abre en nueva ventana)`">
                  {{ imageAttribution.license }}
               </a>.
               <a 
                  :href="imageAttribution.filePageUrl" 
                  target="_blank"
                  aria-label="Ver imagen original en Wikimedia Commons (se abre en nueva ventana)">
                  Ver en Wikimedia Commons
               </a>
            </small>
         </figcaption>
      </figure>
   </div>
</template>

<script>
import { getWikiCommonsImage } from '@/api/wikiCommonsConnectionService.js'

export default {

   name: 'PlayerPhotoByName',

   props: {
      playerName: {
         type: String,
         required: true
      },
      msg: {
         type: String,
         required: true
      },
      alt: {
         type: String,
         required: true
      },
      wikiQuery: {
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
         urlImage: null, 
         imageAttribution: null,
      }
   },

   methods: {
      async getPlayerImage() {
         try {
            // First search
            const res = await getWikiCommonsImage(this.wikiQuery)
            if (res){
               this.urlImage = res.imageUrl
               this.imageAttribution = res.imageAttribution
            } else {
               // Second search in case first one fails
               const res2 = await getWikiCommonsImage(this.playerName)
               if (res2){
                  this.urlImage = res2.imageUrl
                  this.imageAttribution = res2.imageAttribution
               }
            }

         } catch (err) {
            console.error(`Error retrieving WikiCommons ${this.playerName} image: ${err}`)
         }
      },
   },

   async mounted() {
      await this.getPlayerImage()
   }
}
</script>

<style scoped>
   figure {
      max-width: 500px;
   }

   .photo {
      border: 1px solid #140202;
      width: auto;
      max-height: 520px;
   }

   .fixed-height {
      height: 300px;
      width: auto;
      max-width: 100%;
      object-fit: contain;
      border: none;
   }
</style>