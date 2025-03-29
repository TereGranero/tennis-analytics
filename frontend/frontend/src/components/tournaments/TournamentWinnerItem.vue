<template>
   <tr>
      <!-- Year -->
      <td class="text-center">
         {{ winner.year }}
      </td>

      <!-- Player fullname and flag -->
      <td 
         @click="$emit('view-player', winner.winner_id)" >
         <img
            v-if="winner.winner_country !== 'unknown'"
            :src="'https://flagcdn.com/w40/' + winner.winner_country + '.png'"
            :alt="winner.winner_country"
            :title="winner.winner_country"
            class="flag ms-5 me-2"> 
         <span class="cursor-pointer">{{ winner.winner_fullname }}</span>
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
