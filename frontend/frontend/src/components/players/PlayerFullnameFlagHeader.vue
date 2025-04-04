<template>

   <!-- Header fullname and flag -->
   <div 
      v-if="player" 
      class="row bg-dark text-white mb-3 mb-md-5"
      aria-labelledby="playerFullnameHeading">

      <div class="d-flex align-items-center justify-content-center w-100">
         <img
            v-if="player.country !== 'unknown' && player.country!== '-'"
            :src="'https://flagcdn.com/w40/' + player.country + '.png'"
            :alt="'Bandera de ' + player.country"
            class="flag me-3"
            aria-hidden="true"> 
            <h1 
               id="playerFullnameHeading" 
               class="text-responsive-2 text-center m-0">
               {{ player.fullname.toUpperCase() }}
            </h1>
      </div>
   </div>

</template>

<script>
export default {

   name: 'PlayerFullnameFlagHeader',

   props: {
      player: Object,
      required: true
   }

}
</script>

<style scoped> 
   .flag {
      width: 30px;
      height: 1.5em;
   }
</style>