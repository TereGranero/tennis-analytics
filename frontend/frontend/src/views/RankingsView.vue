<template>
   <div class="container">

      <!-- Header Image -->
      <div class="row mb-3">
         <div class="col-12">
            <HeaderImage
               imgName="rankings-banner"
               alt="Titulo Rankings" />
         </div>
      </div>

      <!-- Alert Messages -->
      <div 
         class="row" 
         v-if="!rankings.length && isLoading" >

         <div class="col-12">
            <div class="alert alert-info text-responsive-3 text-center" role="alert">
               Cargando rankings...
            </div>
         </div>
      </div>

      <!-- Select year -->
      <div 
         class="row justify-content-center align-items-center mb-3 mb-sm-4 mb-md-5" 
         v-if="rankings.length && !isLoading">

         <div class="col-auto">
            <label for="yearToSelect" class="form-label me-2 text-responsive-4">Año:</label>
            <select
               id="yearToSelect"
               class="form-select "
               v-model="yearToShow"
               @change="changeYear">
               <option 
                  v-for="year in years"
                  :key="year"
                  :value="year">
                  {{ year }}
               </option>
            </select>
         </div>
      </div>
     
      <div 
         class="d-flex flex-row flex-wrap align-items-center justify-content-center mb-3 mb-md-4"
         v-if="rankings.length && photoFigcaption && wikiQuery && player1Name && !isLoading">

         <!-- Player No.1 Image -->
         <div class="col-12 col-md-4 mt-3">
            <PlayerPhotoByName 
               :wikiQuery="wikiQuery"
               :playerName="player1Name"
               :msg="photoFigcaption"
               :alt="player1Name" /> 
         </div>

         <!-- Ranking Table -->
         <div class="d-flex ms-md-5">
            <RankingsTable 
               :rankings="rankings"
               @view-player="viewPlayer" /> 
         </div>
      </div>

      <!-- Rankings pages navigation -->
      <div 
         class="row justify-content-center"
         v-if="rankings.length && !isLoading">

         <div class="col-12">
            <Pagination 
               :page="page" 
               :totalPages="totalPages"
               class="text-responsive-4"
               @goToPage="goToPage" />
         </div>
      </div>

   </div>
</template>

<script>
import HeaderImage from '@/components/HeaderImage.vue'
import PlayerPhotoByName  from '@/components/players/PlayerPhotoByName.vue'
import RankingsTable from '@/components/rankings/RankingsTable.vue'
import Pagination from '@/components/Pagination.vue'
import { getEndYearRankings } from '@/api/serverConnectionService.js'

export default {

   name: 'RankingsView',

   components: {
      HeaderImage,
      PlayerPhotoByName ,
      RankingsTable, 
      Pagination
   },

   data() {
      return {
         rankings: [],
         totalRankings: 0,
         page: 1,
         perPage: 10,
         totalPages: 0,
         years: Array.from({ length: 2023 - 1973 + 1 }, (_, index) => 1973 + index),
         yearToShow: 2023,
         numberOne: null,
         isLoading: false,
      }
   },

   computed: {

      wikiQuery() {
         // PlayerImage prop. Needed to searh player in Commons as first search
         if (this.numberOne) {
            return `${this.numberOne.name_first} ${this.numberOne.name_last} ${this.yearToShow.toString()}`
         }
         return null
      },

      player1Name() {
         // PlayerImage prop. Needed to searh player in Commons as second search
         if (this.numberOne) {
            return `${this.numberOne.name_first} ${this.numberOne.name_last}`
         }
         return null
      },

      photoFigcaption() {
         // PlayerImage prop
         if (this.numberOne) {
            return `${this.numberOne.name_first} ${this.numberOne.name_last} - ATP No.1 en ${this.yearToShow.toString()}`
         }
         return null
      }
   },

   methods: {
      async loadRankings() {
         // Retrieve all rankings for selected year, with pagination
         
         try {
            this.rankings = []
            this.isLoading = true

            const data = await getEndYearRankings(
               this.page, 
               this.perPage,
               this.yearToShow.toString()
            )
            
            if (data.status == 'error') {
               console.error(`Backend response error: ${data.message}`)
               alert('Se ha producido un error y los rankings no se han podido cargar.')
               this.yearToShow= 2023
               this.page = 1
               await this.loadRankings()

            } else {
               this.rankings = data.rankings
               this.totalRankings = data.total_rankings
               this.totalPages = data.pages

               if (this.totalRankings == 0){
                  alert('No se ha encontrado ningún ranking.')
                  this.yearToShow= 2023
                  this.page = 1
                  await this.loadRankings()

               } else {  // ok
                  
                  // Updates No.1
                  if (this.page == 1) {
                     this.numberOne = this.rankings.find(
                        player => player.rank == 1
                     )
                  }
                  this.isLoading = false
                  console.log(`${this.totalRankings} rankings have been retrieved. Page ${this.page} of ${this.totalPages} is shown.`)
               }
            }

         } catch(err) {
            console.error(`Error retrieving rankings: ${err}`)
            alert('Se ha producido un error y los rankings no se han podido cargar.')
            this.yearToShow= 2023
            this.page = 1
            await this.loadRankings()
         }
      },

      async changeYear() {
         this.page = 1
         this.numberOne = null
         await this.loadRankings()
      },

      async goToPage(page) {
         // Rankings pages navigation
         if (page >= 1 && page <= this.totalPages) {
            this.page = page
            await this.loadRankings()
         }
      },

      viewPlayer(id) {
         console.log(`RankingsView sends id ${id} to PlayerView` )
         this.$router.push({ name: 'Player', params: { id } })
      },

   },

   async mounted() {
      await this.loadRankings()
   }

}
</script>

<style></style>