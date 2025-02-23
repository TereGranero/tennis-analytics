<template>
   <div class="row justify-content-center mt-5">
      <div class="col-md-12 justify-content-center align-items-center">
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
            title: {
               text: 'ATP Ranking'
            },
            tooltip: { // shows value as moving through axis
               trigger: 'axis'
            },
            xAxis: {
               name: 'Año',
               type: 'category',
               data: this.ranksByYear.map(rankObject=> rankObject.year)
            },
            yAxis: {
               name: 'Ranking',
               type: 'value',
               min: 1,
               inverse: true
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
 