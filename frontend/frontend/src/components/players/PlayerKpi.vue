<template>
   <div 
      v-if="value != '-'"
      class="card h-100">
     <div class="card-body text-center">
       <h5 class="card-title text-muted mb-2">{{ title }}</h5>
       <h2 class="text-responsive-1 mb-0 fw-bold">{{ value }}{{ percentage ? '%' : '' }}</h2>
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