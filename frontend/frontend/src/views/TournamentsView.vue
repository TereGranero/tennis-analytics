<template>
   <main class="container">

      <!-- Heading -->
      <h1 
         id="tournamentHeading" 
         class="text-center text-green text-responsive-1 mb-5">
         torneos
      </h1>

      <!-- Alert Messages -->
      <section
         class="row" 
         v-if="!tournaments.length && isLoading">

         <div class="col-12">
            <div 
               class="alert alert-info text-responsive-3 text-center" 
               role="status"
               aria-live="polite"
               :aria-busy="!tournaments.length && isLoading">
               Cargando torneos...
            </div>
         </div>
      </section>

      <!-- Select level -->
      <section aria-labelledby="formHeading">
         <h2 id="formHeading" class="visually-hidden">Selección del nivel de los torneos</h2>
         <p 
            id="formInstructions" 
            class="text-responsive-4 text-center mb-5">
            Selecciona el nivel de los torneos:
         </p>

         <form
            class="row justify-content-center align-items-center text-responsive-5 mb-3 mb-sm-4 mb-md-5" 
            v-if="tournaments.length && !isLoading"
            aria-describedby="formInstructions">

            <div 
               class="col-auto"
               role="group" 
               aria-labelledby="levelLabel">
               <label
                  id="levelLabel"
                  for="levelToSelect" 
                  class="form-label me-2">
                  Nivel:
               </label>
               <select
                  id="levelToSelect"
                  class="form-select border-dark bg-transparent text-dark text-responsive-4"
                  v-model="levelToShow"
                  @change="loadTournaments">
                  <option 
                     v-for="level in levels"
                     :key="level"
                     :value="level">
                     {{ level }}
                  </option>
               </select>
            </div>
         </form>
      </section>

      <!-- Tournaments Table Component -->
      <section
         class="row justify-content-center mb-3 mb-md-4"
         v-if="tournaments.length && !isLoading">

         <div class="col-12 col-md-8">
            <TournamentsTable 
               :tournaments="tournaments"
               @view-winners="viewWinners" /> 
         </div>
      </section>

      <!-- Tournaments pages navigation -->
      <nav
         class="row justify-content-center"
         v-if="tournaments.length && !isLoading"
         aria-label="Navegar por las páginas">

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
import TournamentsTable from '@/components/tournaments/TournamentsTable.vue'
import Pagination from '@/components/Pagination.vue'
import { getTournamentsByLevel } from '@/api/serverConnectionService.js'
import { convertIntoSlug } from '@/services/normalization_services.js'

export default {

   name: 'TournamentsView',

   components: {
      TournamentsTable,
      Pagination
   },

   data() {
      return {
         levels: [
            'Grand Slam',
            'Masters 1000',
            'Other ATP',
            'ATP Finals',
            'Olympics'
         ],
         tournaments: [],
         totalTournaments: 0,
         page: 1,
         perPage: 10,
         totalPages: 0,
         levelToShow: 'Grand Slam',
         isLoading: false,
      }
   },

   computed: {
      levelSlug() {
         return convertIntoSlug(this.levelToShow)
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
      async loadTournaments() {
         // Retrieve all tournaments for selected level, with pagination
         
         try {
            this.tournaments = []
            this.isLoading = true

            const data = await getTournamentsByLevel(
               this.page, 
               this.perPage,
               this.levelSlug
            )
            
            if (data.status == 'error') {
               console.error(`Backend response error: ${data.message}`)
               alert('Se ha producido un error y los torneos no se han podido cargar.')
               this.levelToShow= 'Grand Slam'
               this.page = 1
               await this.loadTournaments()

            } else {
               this.tournaments = data.tournaments
               this.totalTournaments = data.total_tournaments
               this.totalPages = data.pages
               console.log(`${this.totalTournaments} tournaments have been retrieved. Page ${this.page} of ${this.totalPages} is shown.`)

               if (this.totalTournaments == 0){
                  alert('No se ha encontrado ningún torneo.')
                  this.levelToShow= 'Grand Slam'
                  this.page = 1
                  await this.loadTournaments()

               } else {  // ok
                  this.isLoading = false
               }
            }

         } catch(err) {
            console.error(`Error retrieving tournaments: ${err}`)
            alert('Se ha producido un error y los torneos no se han podido cargar.')
            this.levelToShow= 'Grand Slam'
            this.page = 1
            await this.loadTournaments()
         }
      },

      async goToPage(page) {
         // Tournaments pages navigation
         if (page >= 1 && page <= this.totalPages) {
            this.page = page
            await this.loadTournaments()
         }
      },

      viewPlayer(id) {  //just in case
         console.log(`TournamentsView sends id ${id} to PlayerView` )
         this.$router.push({ name: 'Player', params: { id } })
      },

      viewWinners(tournamentName) {
         const tournamentSlug = convertIntoSlug(tournamentName)
         console.log(`TournamentsView sends tournament ${tournamentSlug} to TournamentWinnersView` )
         this.$router.push({ 
            name: 'TournamentWinners', 
            params: { tournamentSlug } 
         })
      }

   },

   async mounted() {
      await this.loadTournaments()
   }

}
</script>

<style></style>
