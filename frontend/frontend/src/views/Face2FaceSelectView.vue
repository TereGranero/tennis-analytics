<template>
   <div class="container">

      <!-- Conditional Header Image -->
      <div class="row mb-3">
         <div class="col-12">
            <HeaderImage
               imgName="face2face-banner"
               alt="Título face2face" />
         </div>
      </div>

      <!-- Alert Messages 
      <div 
         class="row" 
         v-if="!namePlayers.length" >

         <div class="col-12">
            <div class="alert alert-info text-responsive-3 text-center" role="alert">
               Cargando jugadores...
            </div>
         </div>
      </div>-->

      <!-- Players Form -->
     <Face2FaceForm 
         @send-form="showPlayers"/>
   </div>
</template>
 
<script>
import HeaderImage from '@/components/HeaderImage.vue'
import Face2FaceForm from '@/components/face2face/Face2FaceForm.vue'


export default {

   name: 'Face2FaceSelectView',

   components: { HeaderImage, Face2FaceForm },

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