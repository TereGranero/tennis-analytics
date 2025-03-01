<template>
     <div class="row justify-content-center g-3 mt-5"> 
         <h3 class="col-md-10 mb-3 mt-3">DATOS DE CARRERA</h3>
         <div v-for="kpi in kpis" :key="kpi.title" :class="columnClass">
            <PlayerKpi
               :title="kpi.title"
               :value="kpi.value"/>
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
      columns: {
         type: Number,
         default: 4,
         validator: value => [1, 2, 3, 4, 6].includes(value)
      }
   },

   computed: {
      columnClass() {
         const colMap = {
            1: 'col-10',
            2: 'col-md-5',
            3: 'col-md-3',
            4: 'col-md-3',
            6: 'col-md-3'
         }
         return colMap[this.columns]
      }
   }
 }
 </script>