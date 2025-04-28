<template>
   <!-- Double KPI for players comparison -->
   <article 
      class="card h-100 border-dark"
      aria-labelledby="cardHeading">
      <div class="card-body text-center">
         <h3 
            id="cardHeading"
            class="card-title text-reponsive-4 mb-2">
            {{ title }}
         </h3>
         <p 
            class="text-responsive-1 text-green mb-0 fw-bold"
            :aria-label="`Comparación: ${value1}${percentage ? ' por ciento' : ''} frente a ${value2}${percentage ? ' por ciento' : ''}`">
            {{ value1 }}{{ percentage ? '%' : '' }} - {{ value2 }}{{ percentage ? '%' : '' }}
         </p>
      </div>
   </article>
</template>

<script>
export default {

   name: 'Face2FaceDoubleKpi',

   props: {
      title: {
         type: String,
         required: true
      },
      
      value1: {
         type: [String, Number],
         required: true
      },

      value2: {
         type: [String, Number],
         required: true
      },

      percentage: {
         type: Boolean,
         default: false
      },
   }
}
</script>