<template>
   <div class="container">

      <!-- Conditional Header Image -->
      <div class="row mb-3">
         <div class="col-12">
            <HeaderImage
               imgName="login-banner"
               alt="Título login" />
         </div>
      </div>

      <!-- Login Form -->
     <LoginForm @send-login="sendLogin"/>
   </div>
 </template>
 
 <script>
import HeaderImage from '@/components/HeaderImage.vue'
import LoginForm from '@/components/LoginForm.vue'
import { tokenService } from '@/api/authConnectionService'

 export default {

   name: 'LoginView',

   components: { HeaderImage, LoginForm },

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