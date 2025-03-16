<template>
   <tr>
      <!-- Rank -->
      <td class="text-center">
         {{ ranking.rank }}
      </td>

      <!-- Player fullname and flag -->
      <td 
         @click="$emit('view-player', ranking.player_id)" 
         class="ps-sm-5">
         <img
            v-if="ranking.country !== 'unknown'"
            :src="'https://flagcdn.com/w40/' + ranking.country + '.png'"
            :alt="ranking.country"
            :title="ranking.country"
            class="flag me-2"> 
         <span class="cursor-pointer">{{ ranking.fullname }}</span>
      </td>

      <!-- Points -->      
      <td class="text-center">
         {{ ranking.points }}
      </td>
   </tr>
</template>

<script>
export default {

   name: 'RankingItem',

   props: {
      ranking: {
         type: Object,
         required: true
      }
   },
}
</script>

<style> </style>
