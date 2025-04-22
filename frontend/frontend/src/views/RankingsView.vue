<template>
   <main class="container">

      <!-- Heading -->
      <h1 
         id="rankingsHeading" 
         class="text-center text-green text-responsive-1 mb-5">
         ranking ATP
      </h1>

      <!-- Loading Message -->
      <section
         class="row" 
         v-if="!rankings.length && isLoading">

         <div class="col-12">
            <div 
               class="alert alert-info text-responsive-3 text-center"         
               role="status"
               aria-live="polite"
               :aria-busy="!rankings.length && isLoading">
               Cargando rankings...
            </div>
         </div>
      </section>

      <!-- Select year -->
      <section 
         v-if="rankings.length && !isLoading"
         aria-labelledby="selectHeading">
         <h2 
            id="selectHeading" 
            class="visually-hidden">
            Filtro de año para obtener los rankings
         </h2>
            
         <form 
            class="row justify-content-center align-items-center mb-3 mb-sm-4 mb-md-5"
            @submit.prevent>

            <div class="col-auto">
               <label 
                  id="yearLabel" 
                  for="yearToSelect" 
                  class="form-label me-2 text-responsive-4">
                  Año:
               </label>
               <select
                  id="yearToSelect"
                  class="form-select border-dark bg-transparent tex-dark"
                  v-model="yearToShow"
                  @change="changeYear"
                  aria-labelledby="yearLabel">
                  <option 
                     v-for="year in years"
                     :key="year"
                     :value="year">
                     {{ year }}
                  </option>
               </select>
            </div>
         </form>
      </section>

      <section 
         v-if="photoFigcaption && wikiQuery && player1Name"
         aria-labelledby="rankingsContentTitle">

         <h2 
            id="rankingsContentTitle" 
            class="visually-hidden">
            Contenido de rankings
         </h2>
         <div class="d-flex flex-row flex-wrap align-items-center justify-content-center mb-3 mb-md-4">

            <!-- Player No.1 Image -->
            <div class="col-12 col-md-5 mt-3">
               <PlayerPhotoByName 
                  :wikiQuery="wikiQuery"
                  :playerName="player1Name"
                  :msg="photoFigcaption"
                  :alt="`Foto de ${player1Name}`" /> 
            </div>

            <!-- Ranking Table -->
            <div
               class="col-12 col-md-6"
               aria-labelledby="rankingsTableHeading">
               <h3
                  id="rankingsTableHeading"
                  class="visually-hidden">
                  Tabla de rankings ATP del año seleccionado
               </h3>
               <RankingsTable 
                  :rankings="rankings"
                  @view-player="viewPlayer" /> 
            </div>
         </div>
      </section>

      <!-- Rankings pages navigation -->
      <nav 
         class="row justify-content-center"
         v-if="rankings.length && !isLoading"
         aria-label="Paginación de rankings">

         <div class="col-12">
            <Pagination 
               :page="page" 
               :totalPages="totalPages"
               class="text-responsive-4"
               @goToPage="goToPage" />
         </div>
      </nav>

   </main>
</template>

<script>
import PlayerPhotoByName  from '@/components/players/PlayerPhotoByName.vue'
import RankingsTable from '@/components/rankings/RankingsTable.vue'
import Pagination from '@/components/Pagination.vue'
import { getEndYearRankings } from '@/api/serverConnectionService.js'

export default {

   name: 'RankingsView',

   components: {
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

   /* https://vuejs.org/guide/best-practices/accessibility
   following https://www.w3.org/WAI/WCAG21/Techniques/general/G1.html
   */
   watch: {
      $route() {
         this.$refs.backToTop.focus()
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