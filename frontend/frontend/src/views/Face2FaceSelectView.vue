<template>
   <main class="container">

      <!-- Heading -->
      <h1 
         id="face2faceSelectHeading" 
         class="text-green text-center text-responsive-1 mb-5">
         Face2Face
      </h1>

      <section aria-labelledby="formHeading">
         <h2 
            id="formHeading" 
            class="visually-hidden">
            Selección de jugadores
         </h2>
         <p 
            id="formInstructions" 
            class="text-responsive-4 text-center mb-5">
            Selecciona los dos jugadores que quieres comparar:
         </p>

         <!-- Players Form -->
         <Face2FaceForm 
            @send-form="showPlayers"
            aria-describedby="formInstructions"/>
      </section>

   </main>
</template>
 
<script>
import Face2FaceForm from '@/components/face2face/Face2FaceForm.vue'

export default {

   name: 'Face2FaceSelectView',

   components: {  
      Face2FaceForm 
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

      showPlayers(player1, player2){
         console.log(`Player1: ${player1}, Player2: ${player2}`)
         this.$router.push({
            name: 'Face2FaceShow', 
            params: { player1Id: player1, player2Id: player2 }
         })
      }
   }
}
</script>

<style></style>