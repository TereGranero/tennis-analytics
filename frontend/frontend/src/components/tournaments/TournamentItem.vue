<template>
   <tr>
      <!-- Tournament Name -->
      <td
         @click="$emit('view-winners', tournamentName)" 
         class="text-center cursor-pointer">
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
