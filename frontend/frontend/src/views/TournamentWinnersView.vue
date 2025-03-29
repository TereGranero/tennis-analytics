<template>
   <div class="container">

      <!-- Header Image -->
      <div class="row mb-3">
         <div class="col-12">
            <HeaderImage
               imgName="tournaments-banner"
               alt="Titulo Tournaments" />
         </div>
      </div>


      <!-- Alert Messages -->
      <div 
         class="row" 
         v-if="!winners.length && isLoading" >

         <div class="col-12">
            <div class="alert alert-info text-responsive-3 text-center" role="alert">
               Cargando torneos...
            </div>
         </div>
      </div>


      <div 
         class="row align-items-center justify-content-center mb-3 mb-md-4"
         v-if="tournamentName && !isLoading">

         <!-- Tournament Logo -->
         <div class="col-12 col-md-5">
            <TournamentLogo 
               :tournament="tournamentName"
               :level="tournamentLevel"
               /> 
         </div>

         <!-- Winners Table Component -->
         <div class="col-12 col-md-6">
            <TournamentWinnersTable 
               :winners="winners"
               @view-player="viewPlayer" /> 
         </div>
      </div>

      <!-- Winners pages navigation -->
      <div 
         class="row justify-content-center"
         v-if="winners.length && !isLoading">

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
      HeaderImage,
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
