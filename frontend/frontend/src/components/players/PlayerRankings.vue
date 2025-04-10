<template>
   <section 
      class="d-flex flex-column align-items-start mb-5"
      aria-labelledby="rankingsTitle">
      <h2 
         id="rankingsTitle"
         class="text-responsive-3 fw-bold m-0">
         EVOLUCIÓN RANKING ATP
      </h2>
      <v-chart
         class="chart w-100" 
         :option="ranksChartOption" 
         autoresize
         role="img"
         aria-label="Gráfico de linea que muestra la evolución del ranking ATP del jugador por años."  />
   </section>
</template>
 
<script>
export default {
   
   name: 'PlayerRankings',

   props: {
      ranksByYear: {
         type: Array,
         required: true
      }
   },

   computed: {
      ranksChartOption() {
         return {
            tooltip: { // shows value as moving through axis
               trigger: 'axis'
            },
            xAxis: {
               name: '',
               type: 'category',
               data: this.ranksByYear.map(rankObject=> rankObject.year)
            },
            yAxis: {
               name: 'Ranking',
               type: 'value',
               min: 1,
               inverse: true,
               nameLocation: 'middle',
               nameTextStyle: {
                  padding: [0, 0, 30, 0],
                  fontSize: 14,
               },
               axisLabel: {
                  formatter: function (value) {
                     return value.toLocaleString('es-ES')
                  }
               },
            },
            series: [
               {
                  name: 'Ranking',
                  type: 'line',
                  data: this.ranksByYear.map(rankObject => rankObject.rank),
                  symbol: 'circle',
                  symbolSize: 10,
                  itemStyle: {
                     color: '#d1dd25',
                     borderWidth: 2,
                     borderColor: '#fff'
                  },
                  lineStyle: {
                     width: 3
                  }
               },
            ]
         }
      }
   }
 }
</script>
 
<style scoped>
   .chart {
      height: 400px;
      width: 100%;
   }
</style>
 