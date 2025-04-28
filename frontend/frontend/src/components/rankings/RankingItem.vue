<template>
   <!-- Ranking table row -->
   <tr>
      <!-- Rank -->
      <td class="text-center">
         {{ playerRow.rank }}
      </td>

      <!-- Player fullname and flag -->
      <td
         @click="$emit('view-player', playerRow.player_id)"
         @keydown.enter="$emit('view-player', playerRow.player_id)"
         class="d-flex align-items-center text-decoration-none ps-sm-5"
         tabindex="0"
         role="button"
         :aria-label="`Ir a la ficha de ${playerRow.fullname}`">
         <img
            v-if="playerRow.country !== 'unknown'"
            :src="'https://flagcdn.com/w40/' + playerRow.country + '.png'"
            :alt="`Bandera de ${playerRow.country}`"
            class="flag me-2"> 
         {{ playerRow.fullname }}

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
