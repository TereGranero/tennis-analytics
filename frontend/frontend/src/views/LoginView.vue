<template>
   <main class="container">

      <!-- Heading -->
      <h1 
         id="loginHeading" 
         class="text-center text-green text-responsive-1 mb-5">
         área privada
      </h1>

      <!-- Login Form -->
      <section aria-labelledby="loginHeading">
         <LoginForm 
            @send-login="sendLogin"
            aria-labelledby="loginHeading"/>
      </section>

   </main>
</template>
 
<script>
import LoginForm from '@/components/LoginForm.vue'
import { tokenService } from '@/api/authConnectionService'

export default {

   name: 'LoginView',

   components: { LoginForm },

   /* https://vuejs.org/guide/best-practices/accessibility
   following https://www.w3.org/WAI/WCAG21/Techniques/general/G1.html
   */
   watch: {
      $route() {
         this.$refs.backToTop.focus()
      }
   },

   methods: {
      async sendLogin(user){
         try{
            const token = await tokenService.login(user)
            if (token) {
               console.log(`Username: ${user.username} has been loggued in successfully!`)
               const redirection = this.$route.query.redirect || '/players'
               this.$router.push(redirection)

            } else {
               console.error(`Error login ${user.username}: ${err}`)
               tokenService.logout()
               alert('No puede acceder al área privada.')
               this.$router.push('/players')
            }
            
         }catch(err){
            console.error(`Error login ${user.username}: ${err}`)
            tokenService.logout()
            alert('No puede acceder al área privada.')
            this.$router.push('/players')
         }
      }
   }
}
</script>

<style></style>