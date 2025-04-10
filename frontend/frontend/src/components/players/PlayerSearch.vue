<template>
   <form
      class="input-group input-group-lg"
      role="search">

      <label 
         for="playerSearch" 
         class="visually-hidden">
         Buscar jugador
      </label>
      <input 
         id="playerSearch"
         type="search" 
         class="form-control border-dark bg-transparent text-dark" 
         :class="{'is-invalid': invalidLastName}" 
         v-model="lastNameToSearch" 
         @focus="resetState" 
         @input="resetState"
         @keydown.enter="search"
         placeholder="Buscar por apellido"
         :aria-invalid="invalidLastName"
         aria-describedby="searchError" />
      <button 
         class="btn btn-outline-dark btn-lg" 
         @click="search"
         aria-label="Buscar jugador">
         Buscar
      </button>
      
      <!-- Error message -->
      <div 
         v-if="invalidLastName" 
         id="searchError"
         class="invalid-feedback"
         role="alert">
         Debes escribir el apellido del tenista que buscas
      </div>
   </form>
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
 