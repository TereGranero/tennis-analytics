<template>
   <table class="table table-hover text-responsive-4">
      <thead>
         <tr>
            <th scope="col-4">Jugador</th>
            <th scope="col-2">País</th>
            <th scope="col-4">Nacimiento</th>
            <th 
               v-if="isAdmin"
               scope="col-2"></th>
         </tr>
      </thead>
      <tbody>
         <PlayerItem 
            v-for="player in players" 
            :key="player.id"
            :playerRow="player"
            :isAdmin="isAdmin"
            class="text-responsive-4"
            @view-player="viewPlayer"
            @edit-player="editPlayer"
            @delete-player="deleteOnePlayer" /> 
      </tbody>
   </table>
</template>

<script>
import PlayerItem from './PlayerItem.vue'

export default {

   name: 'PlayersList',

   components: { PlayerItem },

   props: {
      players: {
         type: Array,
         required: true
      },
      isAdmin: {
         type: Boolean,
         required: true
      }
   },
   
   methods:{
      viewPlayer(id){
         this.$emit('view-player',id)
      },

      editPlayer(id){
         this.$emit('edit-player',id)
      },

      deleteOnePlayer(id){
         this.$emit('delete-player', id)
      },
   },
}
</script>

<style></style>
