<template>
   <!-- Titles table row -->
   <tr>
      <!-- Player fullname and flag -->
      <td 
         @click="$emit('view-player', playerRow.player_id)" 
         class="ps-sm-5">
         <img
            v-if="playerRow.country !== 'unknown'"
            :src="'https://flagcdn.com/w40/' + playerRow.country + '.png'"
            :alt="playerRow.country"
            :title="playerRow.country"
            class="flag me-2"> 
         <span class="cursor-pointer">{{ playerRow.fullname }}</span>
      </td>

      <!-- Titles -->      
      <td class="text-center">
         {{ playerRow.titles }}
      </td>
   </tr>
</template>

<script>
export default {

   name: 'TitleItem',

   props: {
      playerRow: {
         type: Object,
         required: true
      }
   },
}
</script>

<style> </style>
