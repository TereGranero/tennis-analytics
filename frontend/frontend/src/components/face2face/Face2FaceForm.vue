<template>

   <form 
      class="d-flex flex-column align-items-center gap-3 gap-md-5 text-responsive-5 text-green mb-5"
      @submit.prevent="sendForm">

      <!-- Player1 -->
      <div class="col-12 col-md-5">
         <label
            for="player1Select"
            class="form-label">
            Escribe o selecciona el apellido del primer jugador: 
         </label>
         <input
            id="player1Select"
            class="form-control border-dark bg-transparent text-dark text-responsive-4"
            :class="{'is-invalid': processing && invalidPlayer1}"
            v-model="player1"
            @focus="resetState"
            @input="handleInput(1)"
            list="player1List"
            autocomplete="off"
            aria-describedby="player1Help player1Error">
         <datalist id="player1List">
            <option 
               v-for="player in filteredPlayers1" 
               :key="player.player_id" 
               :value="player.fullname">
            </option>
         </datalist>
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
         <input
            id="player2Select"
            class="form-control border-dark bg-transparent text-dark text-responsive-4"
            :class="{'is-invalid': processing && invalidPlayer2}"
            v-model="player2"
            @focus="resetState"
            @input="handleInput(2)"
            list="player2List"
            autocomplete="off"
            aria-describedby="player2Help player2Error">
         <!-- Creates a list of options -->
         <datalist id="player2List">
            <option 
               v-for="player in filteredPlayers2" 
               :key="player.player_id" 
               :value="player.fullname">
            </option>
         </datalist>
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
         searchTimeOut: null
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

            if (data.status === 'error') {
               console.error(`Backend response error: ${data.message}`);

            } else { // ok
               this.namePlayers = data.players

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

      handleInput(playerNum) {
         clearTimeout(this.searchTimeOut)
         
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
         
         } else {
            this.error = true
            console.log('Search name not found.')
         }

      },
      
      resetState(){
         this.error = false
         this.processing = false
      },

      cancelForm(){
         this.player1 = ''
         this.player2 = ''
         this.resetState()
      }
   }
}
</script>

<style scoped>
   form {
      margin-bottom: 2rem
   }
</style>