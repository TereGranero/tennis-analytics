<template>
   <div class="container">
      
      <!-- Search by Last Name -->
      <div class="row mb-5">
         <div class="col-md-5 offset-md-7">
            <PlayerSearch @search-player="searchPlayer" />
         </div>
      </div>

      <!-- Header fullname and flag -->
      <div v-if="player" class="row bg-dark text-white mb-5 mt-3">
         <div class="d-flex align-items-center justify-content-center text-center w-100">
            <img
               v-if="player.country !== 'unknown' && player.country!== '-'"
               :src="'https://flagcdn.com/w40/' + player.country + '.png'"
               :alt="player.country"
               :title="player.country"
               class="flag me-3"> 
            <h2 class="text-center m-0">
               {{ (player.name_first + ' ' + player.name_last).toUpperCase() }}
            </h2>
         </div>
      </div>
      <div v-else class="row">
         <div class="col-md-12">
            <div class="alert alert-info text-center" role="alert">
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
         :columns="3"/>

      <!-- Ranking chart -->
      <PlayerRankings 
         v-if="player"
         :ranksByYear="player.ranks_by_year" />

      <!-- Titles table -->
      <PlayerTitles
         v-if="player && player.titles.length > 0"
         :titles="player.titles" />

   </div>
</template>

<script>
import PlayerSearch from '@/components/PlayerSearch.vue'
import PlayerBio from '@/components/PlayerBio.vue'
import PlayerKpiGrid from '@/components/PlayerKpiGrid.vue'
import PlayerRankings from '@/components/PlayerRankings.vue'
import PlayerTitles from '@/components/PlayerTitles.vue'
import { getPlayerById } from '@/api/connectionService'

export default {

   name: 'PlayerView',

   components: { 
      PlayerSearch,
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
         invalidLastName: false
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
      }
      
   },

   async created() {
      await this.getPlayer()
   },

}
</script>

<style scoped> 
   .flag {
      width: 30px;
      height: 1.5em; 
      vertical-align: middle;
      border: 1px solid #140202;
   }
   h2 {
      height: 1.5em; 
   }
</style>