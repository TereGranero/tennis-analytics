<template>
   <tr>
      <!-- Full Name -->
      <td @click="$emit('view-player', player.player_id)" class="cursor-pointer">
         {{ player.fullname }}
      </td>

      <!-- Flag and country -->
      <td> 
         <img
            v-if="player.country !== 'unknown'"
            :src="'https://flagcdn.com/w40/' + player.country + '.png'"
            :alt="player.country"
            :title="player.country"
            class="flag"> 
         <span v-if="player.country !== 'unknown'"> {{ player.country.toUpperCase() }}</span>
      </td>

      <!-- Birthday -->
      <td>{{ player.birth_date }}</td>

      <!-- Font Awesome Buttons -->
      <td>
         <i class="fas fa-eye text-secondary cursor-pointer me-2" 
            @click="$emit('view-player', player.player_id)" 
            title="Ver"></i>
         <i class="fas fa-edit text-secondary cursor-pointer me-2" 
            @click="$emit('edit-player', player.player_id)" 
            title="Editar"></i>
         <i class="fas fa-trash text-secondary cursor-pointer" 
            @click="$emit('delete-player', player.player_id)" 
            title="Borrar"></i>
      </td>
   </tr>
</template>

<script>
export default {
   props: {
      player: {
         type: Object,
         required: true
      }
   },
}
</script>

<style> 
   .flag {
      width: 30px;
      height: auto;
      margin-right: 10px;
      vertical-align: middle;
      border: 1px solid #140202;
   }

   .cursor-pointer {
      cursor: pointer;
   }
</style>