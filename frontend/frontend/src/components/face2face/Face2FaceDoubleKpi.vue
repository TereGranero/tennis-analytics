<template>
   <article class="card h-100 border-dark">
     <div class="card-body text-center">
       <p class="card-title text-reponsive-4 mb-2">{{ title }}</p>
       <p class="text-responsive-1 text-green mb-0 fw-bold">{{ value1 }}{{ percentage ? '%' : '' }} - {{ value2 }}{{ percentage ? '%' : '' }}</p>
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