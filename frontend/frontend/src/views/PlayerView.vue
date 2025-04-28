<template>
   <!-- Player page -->
   <main class="container">
      
      <!-- Controls -->
      <section
         class="row text-center text-md-end align-items-center mb-3 mb-sm-4 mb-md-5"
         v-if="player"
         role="group"
         aria-label="Controles para jugador">
            
         <!-- Edit Player Button -->
         <div 
            v-if="isAdmin"
            class="col-12 mb-3 col-md-auto mb-md-0">
            <button 
               type="button" 
               class="btn btn-outline-dark btn-lg" 
               @click="editPlayer"
               aria-label="Editar jugador">
               Editar Jugador
            </button>
         </div>

         <!-- Search by Last Name -->
         <div class="col-12 col-md-auto me-md-5">
            <PlayerSearch 
               @search-player="searchPlayer" 
               aria-label="Buscar jugadores por apellido"/>
         </div>
      </section>  <!-- Ends Controls -->

      <!-- Header fullname and flag -->
      <header>
         <PlayerFullnameFlagHeader
            v-if="player" 
            :player="player"/>
            
         <div v-else class="row">
            <div class="col-12">
               <div 
                  class="alert alert-info text-responsive-3 text-center"
                  role="status"
                  aria-live="polite"
                  :aria-busy="!player">
                  Cargando jugador...
               </div>
            </div>
         </div>
      </header>

      <!-- Basic information -->
      <PlayerBio 
         v-if="player"
         :player="player" />

      <!-- KPIs -->
      <PlayerKpiGrid 
         v-if="player"
         :kpis="kpiData"
         titleGrid="DATOS DE CARRERA" />

      <!-- Ranking chart -->
      <PlayerRankings 
         v-if="player && player.ranks_by_year.length > 0 && player.ranks_by_year != '-'"
         :ranksByYear="player.ranks_by_year" />

      <!-- Titles table -->
      <PlayerTitles
         v-if="player && player.titles.length > 0 && player.titles != '-'"
         @view-tournament="viewTournament"
         :titles="player.titles" />

   </main>
</template>

<script>
import PlayerSearch from '@/components/players/PlayerSearch.vue'
import PlayerFullnameFlagHeader from '@/components/players/PlayerFullnameFlagHeader.vue'
import PlayerBio from '@/components/players/PlayerBio.vue'
import PlayerKpiGrid from '@/components/players/PlayerKpiGrid.vue'
import PlayerRankings from '@/components/players/PlayerRankings.vue'
import PlayerTitles from '@/components/players/PlayerTitles.vue'
import { getPlayerById } from '@/api/serverConnectionService.js'
import { convertIntoSlug } from '@/services/normalization_services'
import { tokenService } from "@/api/authConnectionService.js"

export default {

   name: 'PlayerView',

   components: { 
      PlayerSearch,
      PlayerFullnameFlagHeader,
      PlayerBio, 
      PlayerKpiGrid, 
      PlayerRankings,
      PlayerTitles
   },

   props: {
      id: String,
      required: true
   },

   data() {
      return {
         player: null,
         lastNameToSearch: '',
         invalidLastName: false,
         isAdmin: false
      }
   },

   computed: {
      kpiData() {
         if (!this.player) {
            return []
         }
         return [
            {
               title: 'Mejor Ranking ATP',
               value: this.player.best_ranking || '-',
               percentage: false
            },
            {
               title: 'Títulos',
               value: this.player.total_titles  || '-',
               percentage: false
            },
            {
               title: 'Grand Slams',
               value: this.player.grand_slams  || '0',
               percentage: false
            },
            {
               title: 'Masters 1000',
               value: this.player.masters1000  || '0',
               percentage: false
            },
            {
               title: 'W/L Ratio',
               value: this.player.w_l  || '-',
               percentage: false
            },
            {
               title: 'Aces',
               value: this.player.aces  || '-',
               percentage: false
            },
            {
               title: 'Aces por partido',
               value: this.player.aces_match  || '-',
               percentage: false
            },
            {
               title: 'Dobles Faltas',
               value: this.player.double_faults  || '-',
               percentage: false
            },
            {
               title: 'Dobles Faltas por partido',
               value: this.player.double_faults_match  || '-',
               percentage: false
            },
            {
               title: 'Puntos ganados con 1er servicio',
               value: this.player.points_on_first  || '-',
               percentage: false
            },
            {
               title: 'Puntos con 1er servicio por partido',
               value: this.player.points_on_first_match  || '-',
               percentage: false
            },
            {
               title: 'Juegos ganados al saque',
               value: this.player.games_on_serve  || '-',
               percentage: false
            },
            {
               title: 'Juegos al saque por partido',
               value: this.player.games_on_serve_match  || '-',
               percentage: false
            },
            {
               title: '1er servicio dentro',
               value: this.player.first_in  || '-',
               percentage: false
            },
            {
               title: '1er servicio dentro por partido',
               value: this.player.first_in_match  || '-',
               percentage: false
            },
            {
               title: 'Puntos de rotura encarados',
               value: this.player.bp_faced  || '-',
               percentage: false
            },
            {
               title: 'Puntos de rotura salvados',
               value: this.player.bp_saved_percentage || '-',
               percentage: true
            },
         ]
      },
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
      async getPlayer() {
         try {
            const data = await getPlayerById(this.id)
      
            if (data.status == 'error') {
               console.error(`Backend response error: ${data.message}`)
      
            } else {
               this.player = { ...data.player }
               console.log(`Player retrieved: ${JSON.stringify(this.player, null, 2)}`)
            }
         } catch (err) {
            console.error(`Error retrieving player id ${this.id}: ${err}`)
         }
      },

      searchPlayer(lastName) {
         console.log(`PlayerView pushes name_last ${lastName} to PlayersView`)
         this.$router.push({ name: 'Players', params: { lastname: lastName } })
      },

      editPlayer() {
         console.log(`PlayerView sends id ${this.id} to EditPlayerView` )
         this.$router.push({ name: 'EditPlayer', params: { id: this.id } }) 
      },

      viewTournament(tournamentName) {
         let tournamentSlug = convertIntoSlug(tournamentName)
         console.log(`PlayerView sends tournament ${tournamentSlug} to TournamentWinnersView` )
         this.$router.push({ 
            name: 'TournamentWinners', 
            params: { tournamentSlug } 
         })
      },

   },

   async created() {
      this.isAdmin = tokenService.isLoggedIn()
      await this.getPlayer()
   },

}
</script>

<style> </style>
