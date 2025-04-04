<template>
   <div>
      <!-- Tournament logo -->
      <figure 
         v-if="urlTournamentLogo"  
         class="text-center">
         <img
            :src="urlTournamentLogo" 
            :alt="`Logo Torneo ${tournament}`" 
            class="img-fluid logo" />
         
         <!-- Attribution -->
         <figcaption 
            v-if="logoFound"
            class="mt-2 text-muted text-break w-40">
            <span class="fw-bold">{{ tournament }}</span> <br>
            <small>
               "<span v-html="imageAttribution.title" ></span>" por <span v-html="imageAttribution.author"></span>,
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
                  Wikimedia Commons
               </a>
            </small>
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
         imageAttribution: null,
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
               const res = await getWikiDataLogo(this.wikidata_id)
               if (res) {
                  this.urlTournamentLogo = res.logoUrl
                  this.imageAttribution = res.imageAttribution
                  this.logoFound = true
                  console.log(`Logo: ${this.urlTournamentLogo}`)
               } else {
                  console.log(`Logo not found in WikiData`)
                  this.getGenericLogo()
               }
               
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
         //console.log(this.level)
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
