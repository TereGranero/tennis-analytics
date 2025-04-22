<template>
   <div
      class="card h-100 border-dark"
      role="region"
      :aria-label="`${title}: ${value}${percentage ? '%' : ''}`">

      <div class="card-body text-center">
         <p class="card-title text-reponsive-4 mb-2">
            {{ title }}
         </p>
         <p class="text-responsive-1 text-green mb-0 fw-bold">
            {{ value }}{{ percentage ? '%' : '' }}
         </p>
      </div>
   </div>
</template>

<script>
export default {

   name: 'PlayerKpi',

   props: {
      title: {
         type: String,
         required: true
      },
      
      value: {
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