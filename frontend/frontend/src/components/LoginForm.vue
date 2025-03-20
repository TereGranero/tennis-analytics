<template>
   <form 
      class="d-flex flex-column align-items-center gap-3 gap-md-5 text-responsive-4"
      @submit.prevent="sendForm">

      <!-- Username -->
      <div class="col-12 col-md-5">
         <label
            for="usernameInput"
            class="form-label">
            Usuario: 
         </label>
         <input
            id="usernameInput"
            type="text" 
            class="form-control"
            :class="{'is-invalid': processing && invalidUsername}"
            @focus="resetState"
            v-model="user.username">
         <div v-if="processing && invalidUsername" class="invalid-feedback">
            Debes rellenar el campo Usuario
         </div>
      </div>

      <!-- Password -->
      <div class="col-12  col-md-5">
         <label 
            for="passwordInput" 
            class="form-label">
            Contraseña: 
         </label>
         <input 
            id="passwordInput"
            type="password" 
            class="form-control"
            :class="{'is-invalid': processing && invalidPassword}"
            @focus="resetState"
            v-model="user.password">
         <div 
            v-if="processing && invalidPassword" 
            class="invalid-feedback">
            Debes rellenar el campo Contraseña
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

   name: 'LoginForm',

   data() {
      return {
         user: {
            username: '',
            password: '',
         },
         processing: false,
         error: false,
         imgName: 'login-banner',
         alt: 'Título login'
      }
   },

   computed: {
      // --------------------------- Validates Form ---------------------------
      invalidUsername() {
         return this.user.username < 1
      },

      invalidPassword() {
         return this.user.password < 1
      },
   },

   methods: {
      sendForm() {
         this.processing = true
         this.resetState()

         // Validates fields
         if(this.invaliduserName || 
            this.invalidPassword ) {
               this.error = true
               return
         }

         // Sends events
         console.log('Login sent')
         this.$emit('send-login', this.user)
   

         // Resets form and variables
         this.user = {
            username: '',
            password: '',
         },
         this.processing = false
         this.error = false
      },
      
      resetState(){
         this.error = false
      },

      cancelForm(){
         this.$router.push('/')
      }
   }
}
</script>

<style scoped>
   form {
      margin-bottom: 2rem;
   }
</style>