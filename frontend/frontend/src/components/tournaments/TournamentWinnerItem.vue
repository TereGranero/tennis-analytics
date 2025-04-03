<template>
   <tr>
      <!-- Year -->
      <td class="text-center">
         {{ winner.year }}
      </td>

      <!-- Player fullname and flag -->
      <td class="ps-sm-5">
         <button 
            @click="$emit('view-player', winner.winner_id)" 
            class="btn btn-link p-0 d-flex align-items-center text-decoration-none"
            :aria-label="`Ir a la ficha de ${winner.winner_fullname}`">

            <img
               v-if="winner.winner_country !== 'unknown'"
               :src="'https://flagcdn.com/w40/' + winner.winner_country + '.png'"
               :alt="`Bandera de ${winner.winner_country}`"
               class="flag ms-5 me-2"> 
            <span class="cursor-pointer">{{ winner.winner_fullname }}</span>
         </button>
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
