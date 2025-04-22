<template>
   <table class="table table-hover text-responsive-4">
      <caption class="visually-hidden">
         Tabla de ranking ATP con el jugador, su ranking y puntos conseguidos en el año seleccionado.
      </caption>
      <thead>
         <tr class="text-center">
            <th scope="col" class="col-3">Ranking</th>
            <th scope="col" class="col-6">Jugador</th>
            <th scope="col" class="col-3">Puntos</th>
         </tr>
      </thead>
      <tbody>
         <RankingItem
            v-for="(rk, index) in rankings" 
            :key="index"
            :playerRow="rk"
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
 