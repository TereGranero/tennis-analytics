<template>

   <form 
      class="d-flex flex-column align-items-center gap-3 gap-md-5 text-responsive-5 text-green mb-5"
      role="search"
      @submit.prevent="sendForm">

      <!-- Player1 -->
      <div class="col-12 col-md-5">
         <label
            for="player1Select"
            class="form-label">
            Escribe o selecciona el apellido del primer jugador: 
         </label>
         <div class="position-relative">
            <input
               id="player1Select"
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               :class="{'is-invalid': processing && invalidPlayer1}"
               v-model="player1"
               @focus="() => { resetState(); showSuggestions1 = true }"
               @input="handleInput(1)"
               @blur="hideSuggestionsWithDelay"
               autocomplete="off"
               role="combobox"
               aria-autocomplete="list"
               :aria-expanded="showSuggestions1.toString()"
               aria-owns="player1Options"
               :aria-activedescendant="highlightedPlayer1Id"/>
            <ul 
               v-if="showSuggestions1 && filteredPlayers1.length" 
               id="player1Options"
               class="list-group position-absolute w-100 z-3"
               role="listbox">
               <li 
                  class="list-group-item list-group-item-action"
                  v-for="(player, index) in filteredPlayers1"
                  :key="player.player_id"
                  :id="`player1-option-${index}`"
                  role="option"
                  :aria-selected="index == 0"
                  @mousedown.prevent="selectPlayer(1, player.fullname)">
                  {{ player.fullname }}
               </li>
            </ul>
         </div>
         <div 
            v-if="processing && invalidPlayer1" 
            id="player1Error"
            class="invalid-feedback"
            role="alert">
            Por favor, selecciona un jugador válido del listado.
         </div>
      </div>

      <!-- Player2 -->
      <div class="col-12 col-md-5">
         <label
            for="player2Select"
            class="form-label">
            Escribe o selecciona el apellido del segundo jugador: 
         </label>
         <div class="position-relative">
            <input
               id="player2Select"
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               :class="{'is-invalid': processing && invalidPlayer2}"
               v-model="player2"
               @focus="() => { resetState(); showSuggestions2 = true }"
               @input="handleInput(2)"
               @blur="hideSuggestionsWithDelay"
               autocomplete="off"
               role="combobox"
               aria-autocomplete="list"
               :aria-expanded="showSuggestions2.toString()"
               aria-owns="player2Options"
               :aria-activedescendant="highlightedPlayer2Id"/>
            <ul 
               v-if="showSuggestions2 && filteredPlayers2.length" 
               id="player2Options"
               class="list-group position-absolute w-100 z-3"
               role="listbox">
               <li 
                  class="list-group-item list-group-item-action"
                  v-for="(player, index) in filteredPlayers2"
                  :key="player.player_id"
                  :id="`player2-option-${index}`"
                  role="option"
                  :aria-selected="index == 0"
                  @mousedown.prevent="selectPlayer(2, player.fullname)">
                  {{ player.fullname }}
               </li>
            </ul>
         </div>
         <div 
            v-if="processing && invalidPlayer2" 
            id="player2Error"
            class="invalid-feedback"
            role="alert">
            Por favor, selecciona un jugador válido del listado.
         </div>
      </div>


      <!-- Buttons -->
      <div class="d-flex flex-wrap gap-5 justify-content-center mt-3">
         <div class="form-group">
            <button 
               type="submit"
               class="btn btn-submit btn-lg me-3">
               Aceptar
            </button>
            <button 
               type="button"
               class="btn btn-cancel btn-lg" 
               @click="cancelForm">
               Cancelar
            </button>
         </div>
      </div>
   </form>
</template>

<script>
import { getNamePlayers } from '@/api/serverConnectionService'
export default {

   name: 'Face2FaceForm',

   data() {
      return {
         namePlayers: [],
         player1: '',
         player2: '',
         filteredPlayers1: [],
         filteredPlayers2: [],
         processing: false,
         error: false,
         searchTimeOut: null,
         showSuggestions1: false,
         showSuggestions2: false,
      }
   },

   computed: {
      invalidPlayer1() {
         return !this.filteredPlayers1.some(
            player => player.fullname == this.player1)
      },
      invalidPlayer2() {
         return !this.filteredPlayers2.some(
            player => player.fullname == this.player2)
      },
      highlightedPlayer1Id() {
         return this.filteredPlayers1.length > 0 ? 'player1-option-0' : null
      },
      highlightedPlayer2Id() {
         return this.filteredPlayers2.length > 0 ? 'player2-option-0' : null
      }
   },

   methods: {

      async loadNamePlayers(fullnameToSearch, playerNum) {

         // User did'nt write at least 3 chars. No requesto to backend
         if (fullnameToSearch.length < 3) {
            if (playerNum === 1) {
               this.filteredPlayers1 = []
            } else {
               this.filteredPlayers2 = []
            }
            return
         }

         try {
            const data = await getNamePlayers(fullnameToSearch)

            if (data.status == 'error') {
               console.error(`Backend response error: ${data.message}`);

            } else { // ok
               this.namePlayers = data.players
               console.log(`Data from backend for player ${playerNum}:`, data)

               // Sends backend names to create datalist
               if (playerNum == 1) {
                  this.filteredPlayers1 = this.namePlayers
               } else {
                  this.filteredPlayers2 = this.namePlayers
               }

            }
         } catch (err) {
            console.error(`Error retrieving players: ${err}`)
         }
      },

      selectPlayer(playerNum, name) {
         if (playerNum == 1) {
            this.player1 = name
            this.showSuggestions1 = false
         } else {
            this.player2 = name
            this.showSuggestions2 = false
         }
      },

      hideSuggestionsWithDelay() {
         setTimeout(() => {
            this.showSuggestions1 = false
            this.showSuggestions2 = false
         }, 100)
      },


      handleInput(playerNum) {
         clearTimeout(this.searchTimeOut)

         // Shows the list when writting
         if (playerNum === 1) {
            this.showSuggestions1 = true
         } else {
            this.showSuggestions2 = true
         }
         
         // Sleeps 500ms and searches again
         this.searchTimeOut = setTimeout(() => {
            const fullnameToSearch = playerNum == 1 ? this.player1 : this.player2
            this.loadNamePlayers(fullnameToSearch, playerNum)
         }, 500) 
      },

      sendForm() {
         this.processing = true
         this.resetState()

         // Validates fields
         if (this.invalidPlayer1 || this.invalidPlayer2) {
            this.error = true
            return
         }

         // Find player IDs
         const player1Data = this.filteredPlayers1.find(player => player.fullname == this.player1)
         const player2Data = this.filteredPlayers2.find(player => player.fullname == this.player2)

         if (player1Data && player2Data) {
            // Sends events with player IDs
            console.log(`Players selection has been sent: ${player1Data.player_id} and ${player2Data.player_id}`)
            this.$emit('send-form', player1Data.player_id, player2Data.player_id)

            // Resets form and variables
            this.player1 = ''
            this.player2 = ''
            this.resetState()
            this.processing = false
         
         } else {
            this.error = true
            console.log('Search name not found.')
         }

      },
      
      resetState(){
         this.error = false
      },

      cancelForm(){
         this.player1 = ''
         this.player2 = ''
         this.resetState()
         this.processing = false
      }
   }
}
</script>

<style scoped>
   form {
      margin-bottom: 2rem
   }
</style>