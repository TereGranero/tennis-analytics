<template>
   <div class="container">

      <!-- Header Image -->
      <div class="row mb-3 banner">
         <div class="col-md-12">
            <HeaderImage
               :pageName="pageName" />
         </div>
      </div>

      <!-- Alert Messages -->
      <div 
         class="row mb-3" 
         v-if="!players.length && isSearching" >

         <div class="col-md-12">
            <div class="alert alert-info text-center" role="alert">
               Cargando jugadores...
            </div>
         </div>
      </div>

      <div 
         class="row align-items-center mb-5" 
         v-if="players.length  && !isSearching">

         <!-- Add Player Button -->
         <div class="col-md-6">
            <button 
               type="button" 
               class="btn btn-secondary" 
               @click="addPlayer">
               Añadir Jugador
            </button>
         </div>

         <!-- Search by Last Name -->
         <div class="col-md-5 offset-md-1">
            <PlayerSearch @search-player="searchPlayer" />
         </div>
      </div>

      <!-- PlayersList Component -->
      <div class="row">
         <div class="col-md-12 mb-3">
            <PlayersList 
               :players="players"
               @view-player="viewPlayer"
               @edit-player="editPlayer"
               @delete-player="deleteOnePlayer"
            /> 
         </div>
      </div>

      <!-- Players pages navigation -->
      <div class="row">
         <div class="col-md-12">
            <Pagination 
               :page="page" 
               :totalPages="totalPages" 
               @goToPage="goToPage" />
         </div>
      </div>

   </div>
</template>

<script>
import PlayerSearch from '@/components/PlayerSearch.vue'
import PlayersList from '@/components/PlayersList.vue'
import Pagination from '@/components/Pagination.vue'
import { getAllPlayers, deletePlayer } from '@/api/serverConnectionService.js'

export default {

   name: 'PlayersView',

   components: { 
      PlayerSearch,
      PlayersList, 
      Pagination 
   },

   props: {
      lastname: {
         type: String,
         default: null,
      }
   },


   data() {
      return {
         pageName: 'players',
         players: [],
         totalPlayers: 0,
         page: 1,
         perPage: 12,
         totalPages: 0,
         isSearching: false,
         lastNameToSearch: '',
      }
   },

   computed: {
      isSearchingByLastName() {
         console.log(`Checking if there is a lastname: ${this.lastname}`)
         return this.lastname !== null
      },
   },

   methods: {
      async loadPlayers() {
         // Retrieve all players or filtered players by last name, with pagination
         try {

            this.players = []
            
            const data = await getAllPlayers(
               this.page, 
               this.perPage,
               this.lastNameToSearch
            )
            
            if (data.status == 'error') {
               console.error(`Backend response error: ${data.message}`)
               alert('Se ha producido un error y los jugadores no se han podido cargar.')
               this.lastNameToSearch= ''
               this.page = 1
               await this.loadPlayers()

            } else {
               this.players = data.players
               this.totalPlayers = data.total_players
               this.totalPages = data.pages
               console.log(`${this.totalPlayers} players have been retrieved. Page ${this.page} of ${this.totalPages} is shown.`)

               if (this.totalPlayers == 0){
                  alert('No se ha encontrado ningún jugador.')
                  this.lastNameToSearch= ''
                  this.page = 1
                  await this.loadPlayers()

               } else {  // ok
                  this.isSearching = false
               }
            }

         } catch(err) {
            console.error(`Error retrieving players: ${err}`)
            alert('Se ha producido un error y los jugadores no se han podido cargar.')
            this.lastNameToSearch= ''
            this.page = 1
            await this.loadPlayers()
         }
      },

      searchPlayer(lastName) {
         this.isSearching = true
         this.lastNameToSearch = lastName
         console.log(`Searching by last name: ${this.lastNameToSearch}.`)
         this.page = 1
         this.loadPlayers()
      },

      async goToPage(page) {
         // Players pages navigation
         if (page >= 1 && page <= this.totalPages) {
            this.page = page
            await this.loadPlayers()
         }
      },

      addPlayer() {
         console.log('New player is going to be added')
         this.$router.push({ name: 'AddPlayer'})
      },

      viewPlayer(id) {
         console.log(`PlayersView sends id ${id} to PlayerView` )
         this.$router.push({ name: 'Player', params: { id } })
      },

      editPlayer(id) {
         console.log(`PlayersView sends id ${id} to EditPlayerView` )
         this.$router.push({ name: 'EditPlayer', params: { id } })
      },

      async deleteOnePlayer(id) {
         try {
            await deletePlayer(id)
            this.players = this.players.filter(
               player => player.id != id
            )
            this.totalPlayers--
            console.log(`Player ${id} has been removed successfully`)
            
            if (this.players.length == 0 && this.page > 1) {
               this.page--
               await this.loadPlayers()
            }

         } catch (err) {
            console.error(`Error deleting player id ${id}: ${err}`)
         }
      }
   },

   async mounted() {
      if (this.isSearchingByLastName){
         this.lastNameToSearch = this.lastname
      }
      await this.loadPlayers()
   }

}
</script>

<style>
   .banner img{
      max-width: 100%; 
      height: auto;
   }
</style>