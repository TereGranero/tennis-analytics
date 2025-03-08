<template>
   <div class="card h-100">
     <div class="card-body text-center">
       <h5 class="card-title text-muted mb-2">{{ title }}</h5>
       <h2 class="display-4 mb-0 fw-bold">{{ value }}</h2>
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
      }
   }
 }
 </script>