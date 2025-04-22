<template>
   <main class="container">

      <!-- Heading -->
      <h1 
         id="winnersHeading" 
         class="text-center text-green text-responsive-1 mb-5">
         torneo {{tournamentName}}
      </h1>


      <!-- Alert Messages -->
      <section
         class="row" 
         v-if="!winners.length && isLoading">

         <div class="col-12">
            <div 
               class="alert alert-info text-responsive-3 text-center" 
               role="status"
               aria-live="polite"
               :aria-busy="!winners.length && isLoading">
               Cargando torneos...
            </div>
         </div>
      </section>

      <section
         class="row align-items-center justify-content-center mb-3 mb-md-4"
         v-if="tournamentName && !isLoading"
         aria-labelledby="tournamentsContentTitle">

         <h2 
            id="rankingsContentTitle" 
            class="visually-hidden">
            Contenido de ganadores del torneo seleccionado
         </h2>
         <div class="d-flex flex-row flex-wrap align-items-center justify-content-center mb-3 mb-md-4">

            <!-- Tournament Logo -->
            <div class="col-12 col-md-5 mt-3">
               <TournamentLogo 
                  :tournament="tournamentName"
                  :level="tournamentLevel"
                  /> 
            </div>

            <!-- Winners Table  -->
            <div 
               class="col-12 col-md-6"
               aria-labelledby="tournamentTableHeading">
               <h3
                  id="tournamentTableHeading"
                  class="visually-hidden">
                  Tabla de ganadores del torneo seleccionado
               </h3>
               <TournamentWinnersTable 
                  :winners="winners"
                  @view-player="viewPlayer" /> 
            </div>
         </div>
      </section>

      <!-- Winners pages navigation -->
      <nav
         class="row justify-content-center"
         v-if="winners.length && !isLoading"
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
import TournamentLogo from '@/components/tournaments/TournamentLogo.vue'
import TournamentWinnersTable from '@/components/tournaments/TournamentWinnersTable.vue'
import Pagination from '@/components/Pagination.vue'
import { getTournamentWinners } from '@/api/serverConnectionService.js'

export default {

   name: 'TournamentWinnersView',

   props: {
      tournamentSlug: {
         type: String,
         required: true
      }
   },

   components: {
      TournamentLogo,
      TournamentWinnersTable,
      Pagination
   },

   data() {
      return {
         winners: [],
         totalWinners: 0,
         page: 1,
         perPage: 10,
         totalPages: 0,
         isLoading: false,
         tournamentName: null,
         tournamentLevel: null,
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
      async loadWinners() {
         // Retrieve all winners for tournament slug, with pagination
         
         try {
            this.winners = []
            this.tournamentName = null
            this.isLoading = true

            const data = await getTournamentWinners(
               this.page, 
               this.perPage,
               this.tournamentSlug
            )
            
            if (data.status == 'error') {
               console.error(`Backend response error: ${data.message}`)
               alert('Se ha producido un error y los ganadores no se han podido cargar.')
               this.$router.push({ name: 'Tournaments' })

            } else {
               this.winners = data.winners
               this.totalWinners = data.total_winners
               this.totalPages = data.pages
               console.log(`${this.totalWinners} winners have been retrieved. Page ${this.page} of ${this.totalPages} is shown.`)

               if (this.totalWinners == 0){
                  alert('No se ha encontrado ningún ganador.')
                  this.$router.push({ name: 'Tournaments' })

               } else {  // ok
                  this.tournamentName = this.winners[0].tourney_name
                  this.tournamentLevel = this.winners[0].tourney_level
                  console.log(this.tournamentLevel)
                  this.isLoading = false
               }
            }

         } catch(err) {
            console.error(`Error retrieving winners: ${err}`)
            alert('Se ha producido un error y los ganadores no se han podido cargar.')
            this.$router.push({ name: 'Tournaments' })
         }
      },

      async goToPage(page) {
         // Winners pages navigation
         if (page >= 1 && page <= this.totalPages) {
            this.page = page
            await this.loadWinners()
         }
      },

      viewPlayer(id) {
         console.log(`TournamentsWinnersView sends id ${id} to PlayerView` )
         this.$router.push({ name: 'Player', params: { id } })
      },

   },

   async mounted() {
      await this.loadWinners()
   }

}
</script>

<style></style>
