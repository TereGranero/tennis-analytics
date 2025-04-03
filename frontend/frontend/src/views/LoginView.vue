<template>
   <main class="container">

      <!-- Header Image -->
      <header class="row mb-3">
         <h1 id="loginTitle" class="visually-hidden">{{ alt }}</h1>
         <div class="col-12">
            <HeaderImage
               imgName="login-banner"
               :alt="alt" />
         </div>
      </header>

      <!-- Login Form -->
      <section aria-labelledby="loginTitle">
         <LoginForm 
            @send-login="sendLogin"
            aria-labelledby="loginTitle"/>
      </section>

   </main>
</template>
 
<script>
import HeaderImage from '@/components/HeaderImage.vue'
import LoginForm from '@/components/LoginForm.vue'
import { tokenService } from '@/api/authConnectionService'

export default {

   name: 'LoginView',

   components: { HeaderImage, LoginForm },

   data(){
      return{
         alt: 'Título Login'
      }
   },

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