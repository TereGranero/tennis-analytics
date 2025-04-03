<template>
   <article
      v-if="value != '-'"
      class="card h-100"
      role="region"
      :aria-label="`${title}: ${value}${percentage ? '%' : ''}`">

      <div class="card-body text-center">
         <h5 class="card-title text-muted mb-2">{{ title }}</h5>
         <p class="text-responsive-1 mb-0 fw-bold">{{ value }}{{ percentage ? '%' : '' }}</p>
      </div>
   </article>
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