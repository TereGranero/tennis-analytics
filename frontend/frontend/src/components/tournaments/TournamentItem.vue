<template>
   <tr>
      <!-- Tournament Name -->
      <td
         @click="$emit('view-winners', tournamentName)" 
         @keydown.enter="$emit('view-winners', tournamentName)"
         class="text-center text-responsive-4 text-green cursor-pointer"
         tabindex="0"
         role="button"
         :aria-label="`Ver los ganadores del torneo ${tournamentName}`">
         {{ tournamentName }}
      </td>
   </tr>
</template>

<script>
export default {

   name: 'TournamentItem',

   props: {
      tournamentName: {
         type: String,
         required: true
      }
   },
}
</script>

<style> </style>
