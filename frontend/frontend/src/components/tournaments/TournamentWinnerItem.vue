<template>
   <tr>
      <!-- Year -->
      <td class="text-center">
         {{ winner.year }}
      </td>

      <!-- Player fullname and flag -->
      <td
         @click="$emit('view-player', winner.winner_id)" 
         @keydown.enter="$emit('view-player', winner.winner_id)" 
         class="d-flex align-items-center text-decoration-none"
         tabindex="0"
         role="button"
         :aria-label="`Ir a la ficha de ${winner.winner_fullname}`">
         <img
            v-if="winner.winner_country !== 'unknown'"
            :src="'https://flagcdn.com/w40/' + winner.winner_country + '.png'"
            :alt="`Bandera de ${winner.winner_country}`"
            class="flag ms-5 me-2"> 
         {{ winner.winner_fullname }}
      </td>
   </tr>
</template>

<script>
export default {

   name: 'TournamentWinnerItem',

   props: {
      winner: {
         type: Object,
         required: true
      }
   },
}
</script>

<style> </style>
