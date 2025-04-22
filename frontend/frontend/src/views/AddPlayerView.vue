<template>
     <PlayerForm
         class="mb-5"
         @add-player="addPlayer"/>
 </template>
 
 <script>
 import PlayerForm from '@/components/players/PlayerForm.vue'
 import { createPlayer } from '@/api/serverConnectionService.js'

 export default {

   name: 'AddPlayerView',
   
   components: { PlayerForm },

   /* https://vuejs.org/guide/best-practices/accessibility
   following https://www.w3.org/WAI/WCAG21/Techniques/general/G1.html
   */
   watch: {
      $route() {
         this.$refs.backToTop.focus()
      }
   },

   methods: {
      async addPlayer(player){
         try{
            await createPlayer(player)
            console.log(`Player id: ${player.player_id} has been added successfully!`)
            
         } catch(err){
            console.error(`Error adding player ${player.player_id}: ${err}`)
            alert('Error: ¡El jugador no se ha añadido!')

         } finally {
            this.$router.push('/players')
         }
      }
   }
 }
 </script>

<style></style>