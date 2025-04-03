<template>
   <tr>
      <!-- Rank -->
      <td class="text-center">
         {{ playerRow.rank }}
      </td>

      <!-- Player fullname and flag -->
      <td class="ps-sm-5">
         <button
            @click="$emit('view-player', playerRow.player_id)"
            class="btn btn-link p-0 d-flex align-items-center text-decoration-none"
            :aria-label="`Ir a la ficha de ${playerRow.fullname}`">
            
            <img
               v-if="playerRow.country !== 'unknown'"
               :src="'https://flagcdn.com/w40/' + playerRow.country + '.png'"
               :alt="`Bandera de ${playerRow.country}`"
               class="flag me-2"> 
            <span class="cursor-pointer">{{ playerRow.fullname }}</span>
         </button>
      </td>

      <!-- Points -->      
      <td class="text-center">
         {{ playerRow.points }}
      </td>
   </tr>
</template>

<script>
export default {

   name: 'RankingItem',

   props: {
      playerRow: {
         type: Object,
         required: true
      }
   },
}
</script>

<style> </style>
