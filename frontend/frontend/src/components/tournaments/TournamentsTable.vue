<template>
   <table class="table table-hover text-responsive-4">
      <caption class="visually-hidden">
         Tabla de torneos ATP del nivel seleccionado.
      </caption>
      <tbody aria-live="polite">
         <TournamentItem
            v-for="(tourneyName, index) in tournaments" 
            :key="index"
            :tournamentName="tourneyName"
            class="text-responsive-4"
            @view-winners="viewWinners" />
      </tbody>
   </table>
</template>
 
<script>
import TournamentItem from './TournamentItem.vue'

export default {
   
   name: 'TournamentsTable',

   components: { TournamentItem },

   props: {
      tournaments: {
         type: Array,
         required: true
      }
   },

   methods: {
      viewWinners(tournamentName){
         this.$emit('view-winners', tournamentName)
      },
   }

}
</script>
 
<style></style>
 