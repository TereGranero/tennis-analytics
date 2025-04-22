<template>
      <PlayerForm
         :id="id"
         class="mb-5"
         @edit-player="editPlayer"/>
</template>

<script>
import PlayerForm from '@/components/players/PlayerForm.vue'
import { updatePlayer } from '@/api/serverConnectionService.js'

export default {

   name: 'EditPlayerView',

   components: { PlayerForm },

   props: {
      id: {
         type: String,
         required: true,
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
      async editPlayer(id, player){
         try {
            await updatePlayer(id, player)
            console.log(`Player ${id} has been updated successfully!`)
            this.$router.push('/players')

         } catch(err){
            console.error(`Error updating player ${id}: ${err}`)
            alert('Error: ¡El jugador no se ha actualizado!')
         }
      },
   },

   mounted() {
      console.log('EditPlayerView received id:', this.id);
  }
}
</script>

<style></style>