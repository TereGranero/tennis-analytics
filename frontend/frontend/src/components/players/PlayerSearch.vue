<template>
   <div 
      class="input-group"
      role="search">
      <label 
         for="player-search" 
         class="visually-hidden">
         Buscar jugador
      </label>
      <input 
         id="player-search"
         type="search" 
         class="form-control" 
         :class="{'is-invalid': invalidLastName}" 
         v-model="lastNameToSearch" 
         @focus="resetState" 
         @input="resetState"
         @keydown.enter="search"
         placeholder="Buscar por apellido"
         aria-required="true"
         aria-invalid="invalidLastName"
         aria-describedby="search-error" />
      <button 
         class="btn btn-secondary" 
         @click="search"
         aria-label="Buscar jugador">
         Buscar
      </button>
      
      <!-- Error message -->
      <div 
         v-if="invalidLastName" 
         id="search-error"
         class="invalid-feedback"
         role="alert">
         Debes escribir el apellido del tenista que buscas
      </div>
   </div>
</template>

<script>
export default {
   
   name: 'PlayerSearch',
   
   data() {
      return {
         lastNameToSearch: '',
         invalidLastName: false
      }
   },

   methods: {

      search() {
         if (this.lastNameToSearch.trim() === '') {
            this.invalidLastName = true
         } else {
            this.$emit('search-player', this.lastNameToSearch)
            this.invalidLastName = false
         }
      },

      resetState() {
         this.invalidLastName = false
      }
   }
}
</script>
 
<style> </style>
 