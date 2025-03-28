<template>
   <div class="input-group">
      <input 
         type="text" 
         class="form-control" 
         :class="{'is-invalid': invalidLastName}" 
         v-model="lastNameToSearch" 
         @focus="resetState" 
         @input="resetState"
         @keydown.enter="search"
         placeholder="Buscar por apellido"
      />
      <button 
         class="btn btn-secondary" 
         @click="search">
         Buscar
      </button>
      
      <!-- Error message -->
      <div 
         v-if="invalidLastName" 
         class="invalid-feedback">
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
 