<template>
   <main class="container">

      <!-- Heading -->
      <h1 
         id="playersHeading" 
         class="text-center text-green text-responsive-1 mb-5">
         jugadores
      </h1>

      <!-- Loading Message -->
      <section
         class="row" 
         v-if="!players.length && isSearching">

         <div class="col-12">
            <div 
               class="alert alert-info text-responsive-3 text-center" 
               role="status"
               aria-live="polite"
               :aria-busy="!players.length && isSearching">
               Cargando jugadores...
            </div>
         </div>
      </section>

      <!-- Controls -->
      <section
         class="row text-center text-md-end align-items-center mb-3 mb-sm-4 mb-md-5" 
         v-if="players.length  && !isSearching"
         role="group"
         aria-label="Controles para jugadores">

         <!-- Add Player Button -->
         <div 
            v-if="isAdmin"
            class="col-12 mb-3 col-md-auto mb-md-0">
            <button 
               type="button" 
               class="btn btn-outline-dark btn-lg" 
               @click="addPlayer"
               aria-label="Añadir nuevo jugador">
               Añadir Jugador
            </button>
         </div>

         <!-- Search by Last Name -->
         <div class="col-12 col-md-auto me-md-5">
            <PlayerSearch 
               @search-player="searchPlayer"
               aria-label="Buscar jugadores por apellido" />
         </div>
      </section>

      <!-- Players Table -->
      <section
         class="row justify-content-center mb-3 mb-md-4"
         v-if="players.length && !isSearching"
         aria-labelledby="playersTableHeading">

         <h2 
            id="playersTableHeading" 
            class="visually-hidden">
            Tabla de jugadores
         </h2>
         <div class="col-12 col-lg-12">
            <PlayersTable 
               :players="players"
               :isAdmin="isAdmin"
               @view-player="viewPlayer"
               @edit-player="editPlayer"
               @delete-player="deleteOnePlayer" /> 
         </div>
      </section>

      <!-- Players pages navigation -->
      <nav
         class="row justify-content-center"
         v-if="players.length && !isSearching"
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
import PlayerSearch from '@/components/players/PlayerSearch.vue'
import PlayersTable from '@/components/players/PlayersTable.vue'
import Pagination from '@/components/Pagination.vue'
import { getAllPlayers, deletePlayer } from '@/api/serverConnectionService.js'
import { tokenService } from "@/api/authConnectionService.js"

export default {

   name: 'PlayersView',

   components: {
      PlayerSearch,
      PlayersTable, 
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
         players: [],
         totalPlayers: 0,
         page: 1,
         perPage: 12,
         totalPages: 0,
         isSearching: false,
         lastNameToSearch: '',
         isAdmin: false
      }
   },

   computed: {
      isSearchingByLastName() {
         console.log(`Checking if there is a lastname: ${this.lastname}`)
         return this.lastname !== null
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
      async loadPlayers() {
         // Retrieve all players or filtered players by last name, with pagination
         try {
            this.isSearching = true
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

            // Checks if there is any player with the selected lastNameToSearh to avoid error 400
            const checkData = await getAllPlayers(
               1, 
               this.perPage,
               this.lastNameToSearch
            )
            
            // If not, empties lastNameToSearch and load all players
            if (checkData.total_players == 0) {
               console.log("No more players with this last name filter. Resetting filter.")
               this.lastNameToSearch = ''
            }
            
            if (this.players.length == 0 && this.page > 1) {
               this.page--
            }

            await this.loadPlayers()

         } catch (err) {
            console.error(`Error deleting player id ${id}: ${err}`)
         }
      }
   },

   async mounted() {
      if (this.isSearchingByLastName){
         this.lastNameToSearch = this.lastname
      }
      this.isAdmin = tokenService.isLoggedIn()
      await this.loadPlayers()
   }

}
</script>

<style></style>