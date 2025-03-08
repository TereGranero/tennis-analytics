<template>
   <nav aria-label="Page navigation" class="text-center">
      <button 
         type="text" 
         class="btn btn-secondary" 
         @click="$emit('goToPage', page - 1)" 
         :disabled="page <= 1">
         Anterior
      </button>

      <span class="mx-3">Página {{ page }} de {{ totalPages }}</span>

      <button 
         type="text" 
         class="btn btn-secondary"
         @click="$emit('goToPage', page + 1)"
         :disabled="page >= totalPages">
         Siguiente
      </button>
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
