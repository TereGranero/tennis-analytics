<template>
   <table class="table table-hover text-responsive-4">
      <thead>
         <tr class="text-center">
            <th scope="col-3">Ranking</th>
            <th scope="col-6">Jugador</th>
            <th scope="col-3">Puntos</th>
         </tr>
      </thead>
      <tbody>
         <RankingItem
            v-for="(rk, index) in rankings" 
            :key="index"
            :ranking="rk"
            class="text-responsive-4"
            @view-player="viewPlayer" />
      </tbody>
   </table>
</template>
 
<script>
import RankingItem from './RankingItem.vue'

export default {
   
   name: 'RankingsTable',

   components: { RankingItem },

   props: {
      rankings: {
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
 