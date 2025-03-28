<template>
   <div class="container">
      
      <div 
         class="row text-center text-md-end align-items-center mb-3 mb-sm-4 mb-md-5"
         v-if="player">
            
         <!-- Edit Player Button -->
         <div 
            v-if="player && isAdmin"
            class="col-12 mb-3 col-md-auto mb-md-0">
            <button 
               type="button" 
               class="btn btn-secondary" 
               @click="editPlayer">
               Editar Jugador
            </button>
         </div>

         <!-- Search by Last Name -->
         <div
            v-if="player"
            class="col-12 col-md-auto me-md-5">
            <PlayerSearch @search-player="searchPlayer" />
         </div>
      </div>

      <!-- Header fullname and flag -->
      <PlayerFullnameFlagHeader
         v-if="player" 
         :player="player"/>
         
      <div v-else class="row">
         <div class="col-12">
            <div class="alert alert-info text-responsive-3 text-center" role="alert">
               Cargando jugador...
            </div>
         </div>
      </div>

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

   </div>
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
               value: this.player.best_ranking || '-'
            },
            {
               title: 'Nº Títulos',
               value: this.player.total_titles  || '-'
            },
            {
               title: 'W/L Ratio',
               value: this.player.w_l  || '-'
            }
         ]
      },
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
