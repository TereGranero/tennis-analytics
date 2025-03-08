<template>
   <div class="row justify-content-center mt-5 mb-5">
      <div class="col-md-10 justify-content-center align-items-center">
         
         <h3 class="mb-3 mt-3">TITULOS TOUR ATP</h3>
         <table class="table table-hover">
            <thead>
               <tr>
                  <th scope="col">Torneo</th>
                  <th scope="col">Año</th>
                  <th scope="col">Superficie</th>
                  <th scope="col">Nivel</th>
               </tr>
            </thead>
            <tbody>
               <tr v-for="(title, index) in titles" :key="index">
                  <td>{{ title.tourney_name }}</td>
                  <td>{{ title.year }}</td>
                  <td>{{ title.surface }}</td>
                  <td>{{ title.tourney_level }}</td>
               </tr>
            </tbody>
         </table>
         
      </div>
   </div>
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
 