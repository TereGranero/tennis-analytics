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
               @change="loadRankings">
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
         class="row align-items-center justify-content-center mb-3 mb-md-4"
         v-if="rankings.length && !isLoading">

         <!-- Player No.1 Image -->
         <div class="col-12 col-md-3">
            <Ranking1Image 
               :player="player1" /> 
         </div>

         <!-- Ranking Table Component -->
         <div class="col-12 col-md-8">
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
import Ranking1Image from '@/components/rankings/Ranking1Image.vue'
import RankingsTable from '@/components/rankings/RankingsTable.vue'
import Pagination from '@/components/Pagination.vue'
import { getEndYearRankings } from '@/api/serverConnectionService.js'

export default {

   name: 'RankingsView',

   components: {
      HeaderImage,
      Ranking1Image,
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
         isLoading: false,
      }
   },

   computed: {
      player1() {
         if (this.rankings.length) {
            return {
               name : `${this.rankings[0].name_first} ${this.rankings[0].name_last}`,
               year: this.yearToShow.toString()
            }
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
               console.log(`${this.totalRankings} rankings have been retrieved. Page ${this.page} of ${this.totalPages} is shown.`)

               if (this.totalRankings == 0){
                  alert('No se ha encontrado ningún ranking.')
                  this.yearToShow= 2023
                  this.page = 1
                  await this.loadRankings()

               } else {  // ok
                  this.isLoading = false
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