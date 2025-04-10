<template>
   <section 
      class="d-flex flex-column align items-start mb-5"
      aria-labelledby="titlesHeading">
      <header>
         <h2 
            id="titlesHeading"
            class="text-responsive-3 fw-bold m-0 mb-5">
            TITULOS TOUR ATP
         </h2>
      </header>

      <table class="table table-hover mt-3">
         <caption class="visually-hidden">
            Tabla de títulos ATP ganados con el año, superficie y nivel del torneo.
         </caption>
         <thead>
            <tr class="text-responsive-4 text-center">
               <th scope="col">Torneo</th>
               <th scope="col">Año</th>
               <th scope="col">Superficie</th>
               <th scope="col">Nivel</th>
            </tr>
         </thead>
         <tbody>
            <tr 
               v-for="(title, index) in titles" 
               :key="index"
               class="text-responsive-4 text-center">
               <td 
                  class="text-start ms-5 cursor-pointer"
                  role="button"
                  tabindex="0"
                  @click="$emit('view-tournament', title.tourney_name)"
                  @keydown.enter="$emit('view-tournament', title.tourney_name)">
                  {{ title.tourney_name }}
               </td>
               <td>
                  {{ title.year }}
               </td>
               <td>
                  {{ title.surface }}
               </td>
               <td>
                  {{ title.tourney_level }}
               </td>
            </tr>
         </tbody>
      </table>
   </section>
</template>
 
<script>
export default {
   
   name: 'PlayerTitles',

   props: {
      titles: {
         type: Array,
         required: true
      }
   },

 }
</script>
 
<style></style>
 