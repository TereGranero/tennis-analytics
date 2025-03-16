<template>
   <div>
      <!-- Tournament logo -->
      <figure 
         v-if="urlTournamentLogo"  
         class="text-center">
         <img
            :src="urlTournamentLogo" 
            alt="Logo Torneo" 
            class="img-fluid logo" />
         <figcaption 
            v-if="logoFound"
            class="mt-2 text-muted">
            {{ tournament }}
         </figcaption>
      </figure>
   </div>
</template>

<script>
import { getWikiDataId, getWikiDataLogo } from '@/api/wikiDataConnectionService.js'

export default {

   name: 'TournamentLogo',

   props: {
      tournament: {
         type: String,
         required: true
      },
      level: {
         type: String,
         required: true,
      }
   },

   data() {
      return {
         urlTournamentLogo: null, 
         wikidata_id: null,
         imagesPath: '/images',
         mappingImage: {
            'Masters 1000': 'masters-1000-logo.jpg',
            'Other ATP': 'atp-tour-logo.jpg',
            'ATP Finals': 'atp-finals-logo.jpg',
            'Olympics': 'olympics-logo.jpg'
         },
         defaultLogo: 'atp-tour-logo.jpg',
         logoFound: false
      }
   },

   methods: {
      async getTournamentLogo() {
         try {
            this.wikidata_id = await getWikiDataId(`${this.tournament}`)

            if (this.wikidata_id) {
               this.urlTournamentLogo = await getWikiDataLogo(this.wikidata_id)
               this.logoFound = true
               console.log(`Logo: ${this.urlTournamentLogo}`)
            } else {
               console.log(`Logo not found in WikiData`)
               this.getGenericLogo()
            }

         } catch (err) {
            console.error(`Error retrieving WikiData tournament logo: ${err}`)
            this.getGenericLogo()
         }
      },

      getGenericLogo() {
         let imageName = this.mappingImage[this.level] || this.defaultLogo
         console.log(this.level)
         this.urlTournamentLogo = `${this.imagesPath}/${imageName}`
         console.log(`Logo: ${this.urlTournamentLogo}`)
      }
   },

   async mounted() {
      await this.getTournamentLogo()
   }
}
</script>

<style scoped>
.logo {
   width: 500px;
   height: auto;
   max-height: 350px;
}
</style>
