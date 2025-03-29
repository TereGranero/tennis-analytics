<template>
   <div class="container">
      
      <!-- Grand Slams Ranking -->

      <!-- Header Image -->
      <div class="col-12 mb-3">
         <HeaderImage
            imgName="grand-slams"
            alt="Título Ranking Grand Slam" />
      </div>

      <div 
         class="d-flex flex-row flex-wrap align-items-start justify-content-center mb-5"
         v-if="rankings['grand-slam'].length && photoFigcaptionGrandSlam && wikiQueryGrandSlam && player1NameGrandSlam && !isLoading['grand-slam']">

         <!-- Player Image -->
         <div class="col-12 col-md-5">
            <PlayerPhotoByName 
               :wikiQuery="wikiQueryGrandSlam"
               :playerName="player1NameGrandSlam"
               :msg="photoFigcaptionGrandSlam"
               :alt="player1NameGrandSlam"
               class="playerImage"  /> 
         </div>

         <!-- Grand Slams Table -->
         <div class="d-flex">
            <TitlesTable 
               :playersRanking="rankings['grand-slam']"
               level="Gran Slams"
               class="col-12 col-md-6 mt-3 ms-md-5"
               @view-player="viewPlayer" /> 
         </div>
      </div>
      <!-- Ends Grand Slams Ranking -->

      <!-- Masters 1000 Ranking -->
      
      <!-- Header Image -->
      <div class="col-12 mb-3">
         <HeaderImage
            imgName="masters-1000"
            alt="Título Ranking Masters 1000" />
      </div>

      <div 
         class="d-flex flex-row flex-wrap align-items-start justify-content-center mb-3 mb-md-5"
         v-if="rankings['masters-1000'].length && photoFigcaptionMasters1000 && wikiQueryMasters1000 && player1NameMasters1000 && !isLoading['masters-1000']">


         <!-- Masters 1000 Table -->
         <div class="d-flex flex-column me-md-5">

            <TitlesTable 
               :playersRanking="rankings['masters-1000']"
               level="Masters 1000"
               class="mt-3"
               @view-player="viewPlayer" /> 
         </div>
         
         <!-- Player Image -->
         <div class="col-12 col-md-5">
            <PlayerPhotoByName  
               :wikiQuery="wikiQueryMasters1000"
               :playerName="player1NameMasters1000"
               :msg="photoFigcaptionMasters1000"
               :alt="player1NameMasters1000"
               class="playerImage" /> 
         </div>
      </div>
      
      <!-- Ends Masters 1000 Ranking -->

      <!-- News -->
      <div class="col-12 mb-3">
         <HeaderImage
            imgName="news"
            alt="Título Noticias" />
      </div>

      <div 
         class="row align-items-center justify-content-center mb-5">
         <TennisNews :totalNews="totalNews" />
      </div>
   </div>
</template>

<script>
import { getRankingTitles } from '@/api/serverConnectionService'
import HeaderImage from '@/components/HeaderImage.vue'
import PlayerPhotoByName  from '@/components/players/PlayerPhotoByName.vue'
import TitlesTable from '@/components/home/TitlesTable.vue'
import TennisNews from '@/components/home/TennisNews.vue'

export default {

   name: 'HomeView',

   components: { 
      PlayerPhotoByName ,
      HeaderImage,
      TitlesTable,
      TennisNews
    },

   data() {
      return {
         totalNews: 6,
         sizeRankings: 5,
         rankings: {
            'grand-slam': [],
            'masters-1000': []
         },
         isLoading: { 
            'grand-slam': true,
            'masters-1000': true
         },
         totalRankings: { 
            'grand-slam': 0,
            'masters-1000': 0
         }
      }
   },

   computed: {

      wikiQueryGrandSlam() {
         // PlayerImage prop. Needed to searh player in Commons as first search
         if (this.rankings['grand-slam'].length) {
            return `${this.rankings['grand-slam'][0].name_first} ${this.rankings['grand-slam'][0].name_last} Grand Slam}`
         }
         return null
      },

      player1NameGrandSlam() {
         // PlayerImage prop. Needed to searh player in Commons as second search
         if (this.rankings['grand-slam'].length) {
            return `${this.rankings['grand-slam'][0].name_first} ${this.rankings['grand-slam'][0].name_last}`
         }
         return null
      },

      photoFigcaptionGrandSlam() {
         // PlayerImage prop
         if (this.rankings['grand-slam'].length) {
            return `${this.rankings['grand-slam'][0].name_first} ${this.rankings['grand-slam'][0].name_last} - Top Grand Slams`
         }
         return null
      },

      wikiQueryMasters1000() {
         // PlayerImage prop. Needed to searh player in Commons as first search
         if (this.rankings['masters-1000'].length) {
            return `${this.rankings['masters-1000'][0].name_first} ${this.rankings['masters-1000'][0].name_last} Indian Wells}`
         }
         return null
      },

      player1NameMasters1000() {
         // PlayerImage prop. Needed to searh player in Commons as second search
         if (this.rankings['masters-1000'].length) {
            return `${this.rankings['masters-1000'][0].name_first} ${this.rankings['masters-1000'][0].name_last}`
         }
         return null
      },

      photoFigcaptionMasters1000() {
         // PlayerImage prop
         if (this.rankings['masters-1000'].length) {
            return `${this.rankings['masters-1000'][0].name_first} ${this.rankings['masters-1000'][0].name_last} - Top Masters 1000`
         }
         return null
      },

   },

   methods: {
      async loadTitlesRanking(level) {
         try {
               this.rankings[level] = []
               this.isLoading[level] = true

            const data = await getRankingTitles(1, this.sizeRankings, level)  //page 1

            if (data.status == 'error') {
               console.error(`Backend response error: ${data.message}`)
               alert(`Se ha producido un error y el ranking ${level} no se ha podido cargar.`)

            } else {
               this.rankings[level] = data.winners
               this.totalRankings[level] = data.total_winners

               if (this.totalRankings[level] == 0){
                  alert(`No se han encontrado datos de ${level}.`)

               } else {  // ok
                  this.isLoading[level] = false
                  console.log(`${this.totalRankings[level]} ${level} winners have been retrieved.`)
               }
            }

         } catch(err) {
            console.error(`Error retrieving ${level} ranking: ${err}`)
            alert(`Se ha producido un error y el ranking ${level} no se ha podido cargar.`)
         }
      },

      viewPlayer(id) {
         console.log(`HomeView sends id ${id} to PlayerView` )
         this.$router.push({ name: 'Player', params: { id } })
      }
   },

   async mounted() {
      await this.loadTitlesRanking('grand-slam')
      await this.loadTitlesRanking('masters-1000')
   }
   
}
</script>

<style></style>
