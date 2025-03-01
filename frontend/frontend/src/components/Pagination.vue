<template>
   <nav aria-label="Page navigation">
      <button 
         type="text" 
         class="btn btn-secondary btn-sm" 
         @click="$emit('goToPage', page - 1)" 
         :disabled="page <= 1">
         Anterior
      </button>

      Página {{ page }} de {{ totalPages }}

      <button 
         type="text" 
         class="btn btn-secondary btn-sm"
         @click="$emit('goToPage', page + 1)"
         :disabled="page >= totalPages">
         Siguiente
      </button>
   </nav>
</template>

<script>
export default {
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
