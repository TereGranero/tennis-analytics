<template>
   <table class="table table-hover text-responsive-4">
      <caption class="visually-hidden">
         Tabla de ganadores del torneo seleccionado por años.
      </caption>
      <thead>
         <tr>
            <th scope="col" class="col-3 text-center">Año</th>
            <th scope="col" class="col-3">Ganador - {{ winners[0].tourney_name.toUpperCase() }}</th>
         </tr>
      </thead>
      <tbody aria-live="polite">
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
 