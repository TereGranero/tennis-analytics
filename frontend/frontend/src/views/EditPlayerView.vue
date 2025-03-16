<template>
  <div>
      <PlayerForm
         :id="id"
         @edit-player="editPlayer"
      />
  </div>
</template>

<script>
import PlayerForm from '@/components/players/PlayerForm.vue'
import { updatePlayer } from '@/api/serverConnectionService.js'

export default {
   components: { PlayerForm },

   props: {
      id: {
         type: String,
         required: true,
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