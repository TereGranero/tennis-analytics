<template>
   <form 
      class="d-flex flex-column align-items-center gap-3 gap-md-5 text-responsive-5 mb-5"
      @submit.prevent="sendForm"
      aria-describedby="loginInstructions">

      <h2 class="visually-hidden">
         Formulario de inicio de sesión para administradores
      </h2>
      <p 
         id="loginInstructions" 
         class="visually-hidden">
         Rellena los campos de usuario y contraseña para acceder a tu cuenta de administrador.
      </p>

      <!-- Username -->
      <div 
         class="col-12 col-md-5"
         role="group" 
         aria-labelledby="usernameLabel">
         <label
            id="usernameLabel"
            for="usernameInput"
            class="form-label">
            Usuario: 
         </label>
         <input
            id="usernameInput"
            type="text" 
            class="form-control border-dark bg-transparent text-dark text-responsive-4"
            :class="{'is-invalid': processing && invalidUsername}"
            @focus="resetState"
            v-model="user.username"
            aria-required="true"   
            :aria-invalid="processing && invalidUsername"
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
         aria-labelledby="passwordLabel">
         <label
            id="passwordLabel"
            for="passwordInput" 
            class="form-label">
            Contraseña: 
         </label>
         <input 
            id="passwordInput"
            type="password" 
            class="form-control border-dark bg-transparent text-dark text-responsive-4"
            :class="{'is-invalid': processing && invalidPassword}"
            @focus="resetState"
            v-model="user.password"
            aria-required="true"
            :aria-invalid="processing && invalidPassword"
            aria-describedby="passwordError">
         <div 
            v-if="processing && invalidPassword"
            id="passwordError"
            class="invalid-feedback"
            role="alert">
            Por favor, rellena el campo Contraseña.
         </div>
      </div>

      <!-- Buttons -->
      <div 
         class="d-flex flex-wrap gap-5 justify-content-center mt-3 mt-md-5"
         role="group">
         <div class="form-group">
            <button 
               type="submit"
               class="btn btn-lg btn-submit me-3">
               Aceptar
            </button>
            <button 
               type="button"
               class="btn btn-lg btn-cancel"
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
      invalidUsername() {
         return this.user.username.trim().length < 1

      },

      invalidPassword() {
         return this.user.password.trim().length < 1

      },
   },

   methods: {
      sendForm() {
         this.processing = true
         this.resetState()

         // Validates fields
         if(this.invalidUsername || 
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
         this.processing = false
      },
      
      resetState(){
         this.error = false
      },

      cancelForm(){
         this.user = {
            username: '',
            password: '',
         },
         this.resetState()
         this.processing = false
      }
   }
}
</script>

<style></style>