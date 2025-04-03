<template>
   <main class="container">

      <!-- Header Image -->
      <header class="row mb-3">
         <div class="col-12">
            <h1 id="face2faceSelectTitle" class="visually-hidden">{{ alt }}</h1>
            <HeaderImage
               imgName="face2face-banner"
               :alt="alt" />
         </div>
      </header>

      <section aria-labelledby="formHeading">
         <h2 id="formHeading" class="visually-hidden">Selección de jugadores</h2>
         <p 
            id="formInstructions" 
            class="text-responsive-4 mb-3">
            Selecciona los dos jugadores que quieres comparar
         </p>

         <!-- Players Form -->
         <Face2FaceForm 
            @send-form="showPlayers"
            aria-describedby="formInstructions"/>
      </section>

   </main>
</template>
 
<script>
import HeaderImage from '@/components/HeaderImage.vue'
import Face2FaceForm from '@/components/face2face/Face2FaceForm.vue'

export default {

   name: 'Face2FaceSelectView',

   components: { 
      HeaderImage, 
      Face2FaceForm 
   },

   data(){
      return {
         alt: 'Título Face2Face'
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