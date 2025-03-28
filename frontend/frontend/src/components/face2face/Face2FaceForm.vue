<template>
   <form 
      class="d-flex flex-column align-items-center gap-3 gap-md-5 text-responsive-4"
      @submit.prevent="sendForm">

      <!-- Player1 -->
      <!--  when input changes, players are filtered and datalist is created -->
      <div class="col-12 col-md-5">
         <label
            for="player1Select"
            class="form-label text-responsive-4">
            Jugador 1: 
         </label>
         <input
            id="player1Select"
            class="form-control text-responsive-4"
            :class="{'is-invalid': processing && invalidPlayer1}"
            v-model="player1"
            @focus="resetState"
            @input="filterPlayers(1)"
            list="player1List"
            autocomplete="off">
         <datalist id="player1List">
            <option 
               v-for="player in filteredPlayers1" 
               :key="player.player_id" 
               :value="player.fullname"/>
         </datalist>
         <div v-if="processing && invalidPlayer1" class="invalid-feedback">
            Debes seleccionar un jugador
         </div>
      </div>

      <!-- Player2 -->
      <div class="col-12 col-md-5">
         <label
            for="player2Select"
            class="form-label text-responsive-4">
            Jugador 2: 
         </label>
         <input
            id="player2Select"
            class="form-control text-responsive-4"
            :class="{'is-invalid': processing && invalidPlayer1}"
            v-model="player2"
            @focus="resetState"
            @input="filterPlayers(2)"
            list="player2List"
            autocomplete="off">
         <!-- Creates a list of options -->
         <datalist id="player2List">
            <option 
               v-for="player in filteredPlayers2" 
               :key="player.player_id" 
               :value="player.fullname"/>
         </datalist>
         <div v-if="processing && invalidPlayer2" class="invalid-feedback">
            Debes seleccionar un jugador
         </div>
      </div>


      <!-- Buttons -->
      <div class="d-flex flex-wrap gap-5 justify-content-center mt-3 mt-md-5">
         <div class="form-group">
            <button 
               type="submit"
               class="btn btn-secondary me-3">
               Aceptar
            </button>
            <button 
               type="button"
               class="btn btn-outline-secondary" 
               @click="cancelForm">
               Cancelar
            </button>
         </div>
      </div>
   </form>
</template>

<script>
export default {

   name: 'Face2FaceForm',

   props: {
      top10Players: {
         type: Array,
         required: true
      }
   },

   data() {
      return {
         player1: '',
         player2: '',
         player1Id: '',
         player2Id: '', 
         filteredPlayers1: [],
         filteredPlayers2: [],
         processing: false,
         error: false
      }
   },

   computed: {
      invalidPlayer1() {
         return !this.top10Players.some(
            player => player.fullname == this.player1)
      },
      invalidPlayer2() {
         return !this.top10Players.some(
            player => player.fullname == this.player2)
      }
   },

   methods: {

      filterPlayers(playerNum) {
         const fullnameToSearch = playerNum == 1 ? this.player1 : this.player2

         const filteredPlayers = this.top10Players.filter(
            player => player.fullname.toLowerCase().includes(fullnameToSearch.toLowerCase())
         )
         if (playerNum == 1) {
            this.filteredPlayers1 = filteredPlayers
         } else {
            this.filteredPlayers2 = filteredPlayers
         }
      },

      resetState() {
         this.processing = false
         this.error = false
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
         const player1Data = this.top10Players.find(player => player.fullname === this.player1)
         const player2Data = this.top10Players.find(player => player.fullname === this.player2)

         if (player1Data && player2Data) {
            // Sends events with player IDs
            console.log(`Players selection has been sent: ${player1Data.player_id} and ${player2Data.player_id}`)
            this.$emit('send-form', player1Data.player_id, player2Data.player_id)

            // Resets form and variables
            this.player1 = ''
            this.player2 = ''
            this.player1Id = '',
            this.player2Id = '', 
            this.resetState()
         
         } else {
            this.error = true
            console.log('Search fullname is not in the list or Top 10 players.')
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