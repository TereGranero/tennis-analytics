<template>
   <div>
      <!-- Player No.1 photo -->
      <figure 
         v-if="urlPlayerImage"  
         class="text-center">
         <img
            :src="urlPlayerImage" 
            alt="ATP Number 1" 
            class="img-fluid photo" />
         <figcaption class="mt-2 text-muted text-break w-40">
            {{ player.name }} - ATP No. 1 en {{ player.year }} <br>
            <small>
               "<span v-html="imageAttribution.title"></span>" por <span v-html="imageAttribution.author"></span>,
               bajo licencia <a :href="imageAttribution.licenseUrl" target="_blank">{{ imageAttribution.license }}</a>.
               <a :href="imageAttribution.filePageUrl" target="_blank">Ver en Wikimedia Commons</a>
            </small>
         </figcaption>
      </figure>
   </div>
</template>

<script>
import { getWikiCommonsImage } from '@/api/wikiCommonsConnectionService.js'

export default {

   name: 'Ranking1Image',

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
      }
   },

   computed: {
      wikiCommonsQuery() {
         if (this.player) {
            console.log(`Query: ${this.player.name} ${this.player.year}`)
            return `${this.player.name} ${this.player.year}`
         } 
         return null
      }
   },

   watch: {
      // Request image only when data is available
      'wikiCommonsQuery': {
         immediate: true, // If value is not null, launches
         handler(newQuery) {
            if (newQuery && newQuery.trim() !== '') {
               this.getPlayer1Image();
            }
         }
      },
   },

   methods: {
      async getPlayer1Image() {
         try {
            const res = await getWikiCommonsImage(this.wikiCommonsQuery)
            if (res){
               this.urlPlayerImage = res.imageUrl
               this.imageAttribution = res.imageAttribution
            } else {
               const res2 = await getWikiCommonsImage(this.player.name)
               if (res2){
                  this.urlPlayerImage = res2.imageUrl
                  this.imageAttribution = res2.imageAttribution
               }
            }

         } catch (err) {
            console.error(`Error retrieving WikiCommons player No.1 image: ${err}`)
         }
      },
   }
}
</script>

<style scoped>
   .photo {
      border: 1px solid #140202;
      width: auto;
      max-height: 650px;
   }
</style>