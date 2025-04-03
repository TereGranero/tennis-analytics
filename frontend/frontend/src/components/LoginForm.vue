<template>
   <form 
      class="d-flex flex-column align-items-center gap-3 gap-md-5 text-responsive-4"
      @submit.prevent="sendForm"
      aria-describedby="login-instructions">

      <h2 class="visually-hidden">Formulario de inicio de sesión para administradores</h2>
      
      <p id="login-instructions" class="visually-hidden">
         Rellena los campos de usuario y contraseña para acceder a tu cuenta de administrador.
      </p>

      <!-- Username -->
      <div 
         class="col-12 col-md-5"
         role="group" 
         aria-labelledby="username-label">
         <label
            id="username-label"
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
            v-model="user.username"
            aria-required="true"   
            aria-invalid="processing && invalidUsername"
            aria-describedby="usernameError">
         <div 
            v-if="processing && invalidUsername" 
            id="usernameError"
            class="invalid-feedback"
            role="alert">
            Por favor, rellena el campo Usuario.
         </div>
      </div>

      <!-- Password -->
      <div 
         class="col-12 col-md-5"
         role="group" 
         aria-labelledby="password-label">
         <label
            id="password-label"
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
            v-model="user.password"
            aria-required="true"
            aria-invalid="processing && invalidPassword"
            aria-describedby="passwordError">
         <div 
            v-if="processing && invalidPassword"
            id="passwordError"
            class="invalid-feedback"
            role="alert">
            Por favor, rellena el campo Contraseña.
         </div>
      </div>


      <!-- Buttons btn-outline-dark-->
      <div 
         class="d-flex flex-wrap gap-5 justify-content-center mt-3 mt-md-5"
         role="group">
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
         error: false
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
         this.resetState()
      },
      
      resetState(){
         this.error = false
         this.processing = false
      },

      cancelForm(){
         this.user = {
            username: '',
            password: '',
         },
         this.resetState()
      }
   }
}
</script>

<style scoped>
   form {
      margin-bottom: 2rem;
   }
</style>