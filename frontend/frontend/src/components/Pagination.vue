<template>
   <!-- Pagination menu -->
   <nav 
      aria-label="Paginación de jugadores" 
      class="mb-5">
      <div class="d-flex flex-wrap justify-content-center align-items-center gap-3">
         <button 
            type="button" 
            class="btn btn-outline-dark btn-lg" 
            @click="$emit('goToPage', page - 1)" 
            :disabled="page <= 1"
            aria-label="Ir a la página anterior"
            :aria-disabled="page <= 1">
            Anterior
         </button>

         <span class="mx-3">Página {{ page }} de {{ totalPages }}</span>

         <button 
            type="button" 
            class="btn btn-outline-dark btn-lg"
            @click="$emit('goToPage', page + 1)"
            :disabled="page >= totalPages"
            aria-label="Ir a la página siguiente"
            :aria-disabled="page >= totalPages">
            Siguiente
         </button>
      </div>
   </nav>
</template>

<script>
export default {

   name: 'Pagination',

   props: {
      page: {
         type: Number,
         required: true
      },
      
      totalPages: {
         type: Number,
         required: true
      }
   }
}
</script>

<style></style>
