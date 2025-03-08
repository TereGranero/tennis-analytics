<template>
   <div class="container">

      <!-- Header Image -->
      <div class="row mb-3 banner">
         <div class="col-md-12">
            <HeaderImage
               imgName="rankings-banner"
               alt="Titulo Rankings" />
         </div>
      </div>


      <!-- Alert Messages -->
      <div 
         class="row mb-3" 
         v-if="!rankings.length" >

         <div class="col-md-12">
            <div class="alert alert-info text-center" role="alert">
               Cargando ranking...
            </div>
         </div>
      </div>

      <div 
         class="row align-items-center" 
         v-if="rankings.length">

         <!-- Select year -->
         <div class="col-6 offset-5 col-sm-4 offset-sm-7 mb-3 mb-md-5">
            <div class="form-group">
               <label class="font-weight-bold text-sm fs-4 text-md fs-3 text-lg fs-2">Año:</label>
               <select
                  class="form-control text-sm fs-5 text-md fs-4 text-lg fs-3"
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
      </div>

      <!-- Ranking Table Component -->
      <div class="row mb-3 mb-md-4">
         <div class="col-12 col-md-8 offset-md-2">
            <RankingsTable 
               :rankings="rankings"
               @view-player="viewPlayer"
            /> 
         </div>
      </div>

      <!-- Players pages navigation -->
      <div class="row">
         <div class="col-12">
            <Pagination 
               :page="page" 
               :totalPages="totalPages"
               class="text-sm fs-5"
               @goToPage="goToPage" />
         </div>
      </div>

   </div>
</template>

<script>
import HeaderImage from '@/components/HeaderImage.vue'
import RankingsTable from '@/components/RankingsTable.vue'
import Pagination from '@/components/Pagination.vue'
import { getEndYearRankings } from '@/api/serverConnectionService.js'

export default {

   name: 'RankingsView',

   components: {
      HeaderImage,
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
      }
   },



   methods: {
      async loadRankings() {
         // Retrieve all rankings for selected year, with pagination
         
         try {

            this.rankings = []
            
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
                  this.isSearching = false
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
      if (this.isSearchingByLastName){
         this.yearToShow = this.lastname
      }
      await this.loadRankings()
   }

}
</script>

<style></style>