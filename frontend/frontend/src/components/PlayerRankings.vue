<template>
   <div class="row justify-content-center mt-5">
      <div class="col-md-10 justify-content-center align-items-center">
         <h3 class="mb-3 mt-3">EVOLUCIÓN RANKING ATP</h3>
         <v-chart class="chart" :option="ranksChartOption" autoresize />
      </div>
   </div>
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
 