<template>
   <form 
      class="d-flex flex-column align-items-center gap-3 gap-md-5 text-responsive-5 text-green mb-5"
      role="search"
      @submit.prevent="sendForm">

      <!-- Campo jugador 1 -->
      <div class="col-12 col-md-5">
         <label for="player1Select" class="form-label">
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
               @keydown="handleKeydown(1, $event)"
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
                  :aria-selected="highlightedIndex1 == index"
                  :class="{ active: highlightedIndex1 == index }"
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

      <!-- Campo jugador 2 -->
      <div class="col-12 col-md-5">
         <label for="player2Select" class="form-label">
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
               @keydown="handleKeydown(2, $event)"
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
                  :aria-selected="highlightedIndex2 == index"
                  :class="{ active: highlightedIndex2 == index }"
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

      <!-- Botones -->
      <div class="d-flex flex-wrap gap-5 justify-content-center mt-3">
         <div class="form-group">
            <button type="submit" class="btn btn-submit btn-lg me-3">Aceptar</button>
            <button type="button" class="btn btn-cancel btn-lg" @click="cancelForm">Cancelar</button>
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
         highlightedIndex1: -1,
         highlightedIndex2: -1,
         processing: false,
         error: false,
         searchTimeOut: null,
         showSuggestions1: false,
         showSuggestions2: false,
      }
   },
   computed: {
      invalidPlayer1() {
         return !this.filteredPlayers1.some(p => p.fullname == this.player1)
      },
      invalidPlayer2() {
         return !this.filteredPlayers2.some(p => p.fullname == this.player2)
      },
      highlightedPlayer1Id() {
         return this.highlightedIndex1 >= 0 ? `player1-option-${this.highlightedIndex1}` : null
      },
      highlightedPlayer2Id() {
         return this.highlightedIndex2 >= 0 ? `player2-option-${this.highlightedIndex2}` : null
      }
   },
   methods: {
      async loadNamePlayers(fullnameToSearch, playerNum) {
         if (fullnameToSearch.length < 3) {
            if (playerNum == 1) this.filteredPlayers1 = []
            else this.filteredPlayers2 = []
            return
         }

         try {
            const data = await getNamePlayers(fullnameToSearch)
            if (data.status == 'error') {
               console.error(`Backend response error: ${data.message}`)
            } else {
               this.namePlayers = data.players
               if (playerNum == 1) {
                  this.filteredPlayers1 = this.namePlayers
                  this.highlightedIndex1 = 0
               } else {
                  this.filteredPlayers2 = this.namePlayers
                  this.highlightedIndex2 = 0
               }
            }
         } catch (err) {
            console.error(`Error retrieving players: ${err}`)
         }
      },

      handleInput(playerNum) {
         clearTimeout(this.searchTimeOut)
         this.searchTimeOut = setTimeout(() => {
            const name = playerNum == 1 ? this.player1 : this.player2
            this.loadNamePlayers(name, playerNum)
         }, 500)
      },

      handleKeydown(playerNum, event) {
         const suggestions = playerNum == 1 ? this.filteredPlayers1 : this.filteredPlayers2
         let index = playerNum == 1 ? this.highlightedIndex1 : this.highlightedIndex2

         if (event.key == 'ArrowDown') {
            index = (index + 1) % suggestions.length
         } else if (event.key == 'ArrowUp') {
            index = (index - 1 + suggestions.length) % suggestions.length
         } else if (event.key == 'Enter' && index >= 0) {
            event.preventDefault()
            this.selectPlayer(playerNum, suggestions[index].fullname)
            return
         }

         if (playerNum == 1) this.highlightedIndex1 = index
         else this.highlightedIndex2 = index
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

      sendForm() {
         this.processing = true
         this.resetState()
         if (this.invalidPlayer1 || this.invalidPlayer2) {
            this.error = true
            return
         }

         const player1Data = this.filteredPlayers1.find(p => p.fullname == this.player1)
         const player2Data = this.filteredPlayers2.find(p => p.fullname == this.player2)

         if (player1Data && player2Data) {
            this.$emit('send-form', player1Data.player_id, player2Data.player_id)
            this.player1 = ''
            this.player2 = ''
            this.resetState()
            this.processing = false
         } else {
            this.error = true
         }
      },

      resetState() {
         this.error = false
         this.highlightedIndex1 = -1
         this.highlightedIndex2 = -1
      },

      cancelForm() {
         this.player1 = ''
         this.player2 = ''
         this.resetState()
         this.processing = false
      }
   }
}
</script>
