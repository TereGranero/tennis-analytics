<template>
   <div class="container text-center py-5">

      <div class="row justify-content-center">
         <div class="col-md-8">
            <h1 class="text-responsive-1 text-green mb-3">404</h1>
            <h2 class=" text-responsive-2 mb-4">Página no encontrada</h2>
            <p class="text-responsive-3 mb-5">Parece que la página que buscas no existe o ha sido movida.</p>
            <router-link 
               to="/" 
               class="btn btn-submit btn-lg">
               Volver a Inicio
            </router-link>
         </div>
      </div>
   </div>
</template>
 
 <script>
 export default {

   name: 'ErrorView',

 }
 </script>
 
 <style> </style>