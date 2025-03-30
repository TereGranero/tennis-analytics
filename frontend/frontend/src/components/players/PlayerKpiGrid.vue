<template>
     <div 
      v-if="hasAnyKpi"
      class="d-flex flex-column align items-start mb-5"> 
         <h2 
            v-if="titleGrid"
            class="text-responsive-3 fw-bold m-0">
            {{titleGrid}}
         </h2>

         <div class="d-flex flex-wrap gap-5 justify-content-center align-items-center mt-3">
            <PlayerKpi
               v-for="kpi in kpis" 
               :key="kpi.title" 
               :title="kpi.title"
               :value="kpi.value"
               :percentage="kpi.percentage"/>
         </div>
      </div>
 </template>
 
 <script>
 import PlayerKpi from './PlayerKpi.vue'
 
 export default {
   
   name: 'PlayerKpiGrid',

   components: { PlayerKpi },

   props: {
      kpis: {
         type: Array,
         required: true
      },
      titleGrid: {
         type: String,
         default: null
      }
   },

   computed: {
    hasAnyKpi() {
      // If any kpi has not value  '-'
      return this.kpis.some(kpi => kpi.value !== '-');
    }
  }

 }
 </script>