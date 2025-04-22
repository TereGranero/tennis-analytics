<template>
   <!-- Titles by top-players table -->
   <table class="table table-hover text-responsive-4">
      <thead>
         <tr class="text-center">
            <th scope="col-6">Jugador</th>
            <th scope="col-3">{{ level }}</th>
         </tr>
      </thead>
      <tbody>
         <TitlesItem
            v-for="(playerRow, index) in playersRanking" 
            :key="index"
            :playerRow="playerRow"
            class="text-responsive-4"
            @view-player="viewPlayer" />
      </tbody>
   </table>
</template>
 
<script>
import TitlesItem from './TitlesItem.vue'

export default {
   
   name: 'TitlesTable',

   components: { TitlesItem },

   props: {
      playersRanking: {
         type: Array,
         required: true
      },
      level: {
         type: String,
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
 