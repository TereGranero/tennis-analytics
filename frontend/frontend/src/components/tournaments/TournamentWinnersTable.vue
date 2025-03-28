<template>
   <table class="table table-hover text-responsive-4">
      <thead>
         <tr>
            <th scope="col-3" class="text-center">Año</th>
            <th scope="col-3">Ganador - {{ winners[0].tourney_name.toUpperCase() }}</th>
         </tr>
      </thead>
      <tbody>
         <TournamentWinnerItem
            v-for="(winner, index) in winners" 
            :key="index"
            :winner="winner"
            class="text-responsive-4"
            @view-player="viewPlayer" />
      </tbody>
   </table>
</template>
 
<script>
import TournamentWinnerItem from './TournamentWinnerItem.vue'

export default {
   
   name: 'TournamentWinnersTable',

   components: { TournamentWinnerItem },

   props: {
      winners: {
         type: Array,
         required: true
      }
   },

   methods: {
      viewPlayer(id){
         this.$emit('view-player', id)
      },
   }

}
</script>
 
<style></style>
 