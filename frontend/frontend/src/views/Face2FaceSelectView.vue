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

      <!-- Alert Messages -->
      <div 
         class="row" 
         v-if="!top10Players.length" >

         <div class="col-12">
            <div class="alert alert-info text-responsive-3 text-center" role="alert">
               Cargando jugadores...
            </div>
         </div>
      </div>

      <!-- Players Form -->
     <Face2FaceForm 
         v-if="top10Players.length"
         :top10Players="top10Players"
         @send-form="showPlayers"/>
   </div>
</template>
 
<script>
import HeaderImage from '@/components/HeaderImage.vue'
import Face2FaceForm from '@/components/face2face/Face2FaceForm.vue'
import { getTop10Players } from '@/api/serverConnectionService'

export default {

   name: 'Face2FaceSelectView',

   components: { HeaderImage, Face2FaceForm },

   data() {
      return {
         top10Players: []
      }
   },

   methods: {
      async loadTop10Players() {
         try {
            this.top10Players = []
            const data = await getTop10Players()

            if (data.status == 'error') {
               console.error(`Backend response error: ${data.message}`)
               alert('Algo ha fallado no se ha podido encontrar ningún jugador.')
               this.$router.push('/')

            } else {
               this.top10Players = data.top10_players
               const totalTop10Players = this.top10Players.length
               console.log(`${totalTop10Players} top 10 players have been retrieved.`)
               if (totalTop10Players == 0) {
                  alert('No se ha encontrado ningún jugador del Top 10.')
                  this.$router.push('/')
               }
            }

         } catch (err) {
            console.error(`Error retrieving top 10 players: ${err}`)
         }
      },

      showPlayers(player1, player2){
         console.log(`Player1: ${player1}, Player2: ${player2}`)
         this.$router.push({
            name: 'Face2FaceShow', 
            params: { player1Id: player1, player2Id: player2 }
         })
      }
   },

   async mounted(){
      await this.loadTop10Players()
   }
}
</script>

<style></style>