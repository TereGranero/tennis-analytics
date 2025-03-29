<template>
   <div class="card h-100">
     <div class="card-body text-center">
       <h5 class="card-title text-muted mb-2">{{ title }}</h5>
       <h2 class="text-responsive-1 mb-0 fw-bold">{{ value1 }}{{ percentage ? '%' : '' }} - {{ value2 }}{{ percentage ? '%' : '' }}</h2>
     </div>
   </div>
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