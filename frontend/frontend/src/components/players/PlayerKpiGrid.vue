<template>
   <section
      v-if="hasAnyKpi"
      class="d-flex flex-column align items-start mb-5"
      :aria-labelledby="titleGrid ? 'kpiTitle' : null"> 

      <header>
         <h2 
            v-if="titleGrid"
            id="kpiTitle"
            class="text-responsive-3 fw-bold m-0 mb-5">
            {{ titleGrid }}
         </h2>
      </header>

      <ul class="d-flex flex-wrap gap-5 justify-content-center align-items-center mt-3 list-unstyled">
         <li 
            v-for="kpi in kpis.filter(kpi => kpi.value && kpi.value != '-')" 
            :key="kpi.title" 
            role="listitem">
            <PlayerKpi
               :title="kpi.title"
               :value="kpi.value"
               :percentage="kpi.percentage"/>
         </li>
      </ul>
   </section>
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