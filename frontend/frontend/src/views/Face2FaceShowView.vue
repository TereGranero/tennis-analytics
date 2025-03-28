<template>
   <div class="container">

      <!-- Conditional Header Image -->
      <div class="row mb-3">
         <div class="col-12">
            <HeaderImage
               imgName="face2face-banner"
               alt="Título face2face" />
         </div>
      </div>

         <!-- Select Button -->
         <div 
            v-if="player1 & player2"
            class="col-12 mb-3 col-md-auto mb-md-0">
            <button 
               type="button" 
               class="btn btn-secondary" 
               @click="selecPlayers">
               Seleccionar
            </button>
         </div>

      <div class="row justify-content-center align-items-start mb-5 mx-mb-3">

         <!-- Player 1 -->
         <div
            v-if="player1"
            class="col-5 d-flex flex-column">

            <!-- Header fullname and flag -->
            <PlayerFullnameFlagHeader
               :player="player1"/>
            
            <!-- Player photo -->
            <div class="d-flex justify-content-center">
               <PlayerPhoto
                  :playerWikidataId="player1.wikidata_id"
                  :setHeight="true"/>   
            </div>
            
         </div>
         <div v-else class="row">
            <div class="col-12">
               <div class="alert alert-info text-responsive-3 text-center" role="alert">
                  Cargando jugador...
               </div>
            </div>
         </div>

         <!-- Player 2 -->
         <div
            v-if="player2"
            class="col-5 d-flex flex-column">

            <!-- Header fullname and flag -->
            <PlayerFullnameFlagHeader
               :player="player2"/>

            <!-- Player photo -->
            <div class="d-flex justify-content-center">
               <PlayerPhoto
                  :playerWikidataId="player2.wikidata_id"
                  :setHeight="true"/>   
            </div>
         </div>
         <div v-else class="row">
            <div class="col-12">
               <div class="alert alert-info text-responsive-3 text-center" role="alert">
                  Cargando jugador...
               </div>
            </div>
         </div>         
      </div>

      <!-- KPIs comparison -->
      <div class="row justify-content-center align-items-start mb-5 mx-mb-3">
         <div
            v-if="player1"
            class="col-5 d-flex flex-column">
            <Face2FaceDoubleKpi
               v-for="kpi in kpiData" 
               :key="kpi.title" 
               :title="kpi.title"
               :value1="kpi.value1"
               :value2="kpi.value2"
               class="mb-3"/>
         </div>
      </div>

   </div>
 </template>
 
<script>
import HeaderImage from '@/components/HeaderImage.vue'
import PlayerPhoto from '@/components/players/PlayerPhoto.vue'
import PlayerFullnameFlagHeader from '@/components/players/PlayerFullnameFlagHeader.vue'
import Face2FaceDoubleKpi from '@/components/face2face/Face2FaceDoubleKpi.vue'
import { getTop10PlayerById } from '@/api/serverConnectionService'

export default {

   name: 'Face2FaceShowView',

   components: { 
      HeaderImage,
      PlayerPhoto,
      PlayerFullnameFlagHeader,
      Face2FaceDoubleKpi
   },

   props: {
      player1Id: {
         type: String,
         required: true
      },
      player2Id: {
         type: String,
         required: true
      },
   },

   data() {
      return {
         player1: null,
         player2: null,
      }
   },

   computed: {
      kpiData() {
         if ((!this.player1) || (!this.player2)) {
            return []
         }
         return [
            {
               title: 'Mejor Ranking ATP',
               value1: this.player1.best_ranking || '-',
               value2: this.player2.best_ranking || '-'
            },
            {
               title: 'Títulos',
               value1: this.player1.total_titles  || '-',
               value2: this.player2.total_titles  || '-'
            },
            {
               title: 'Grand Slams',
               value1: this.player1.grand_slams  || '0',
               value2: this.player2.grand_slams  || '0'
            },
            {
               title: 'Masters 1000',
               value1: this.player1.masters1000  || '0',
               value2: this.player2.masters1000  || '0'
            },
            {
               title: 'W/L Ratio',
               value1: this.player1.w_l  || '-',
               value2: this.player2.w_l  || '-'
            },
            {
               title: 'Aces',
               value1: this.player1.aces  || '-',
               value2: this.player2.aces  || '-'
            },
            {
               title: 'Dobles Faltas',
               value1: this.player1.double_faults  || '-',
               value2: this.player2.double_faults  || '-'
            },
            {
               title: 'Puntos ganados con 1er servicio',
               value1: this.player1.points_on_first  || '-',
               value2: this.player2.points_on_first  || '-'
            },
            {
               title: 'Puntos ganados con 2º servicio',
               value1: this.player1.points_on_second  || '-',
               value2: this.player2.points_on_second  || '-'
            },
            {
               title: 'Juegos ganados al saque',
               value1: this.player1.games_on_serve  || '-',
               value2: this.player2.games_on_serve  || '-'
            },
            {
               title: '1er servicio dentro',
               value1: this.player1.first_in  || '-',
               value2: this.player2.first_in  || '-'
            },
            {
               title: 'Puntos de rotura encarados',
               value1: this.player1.bp_faced  || '-',
               value2: this.player2.bp_faced  || '-'
            },
            {
               title: 'Puntos de rotura salvados',
               value1: this.player1.bp_saved  || '-',
               value2: this.player2.bp_saved  || '-'
            },
         ]
      },
   },

   methods: {

      async loadPlayer(playerId, playerNum) {
         try {
            const data = await getTop10PlayerById(playerId)

            if (data.status == 'error') {
               console.error(`Backend response error for player id ${playerId}: ${data.message}`)
               alert('Las estadísticas no se han podido cargar')
               this.$route.push({ name:'Face2FaceSelect' })
      
            } else if (playerNum == 1) {
               this.player1 = { ...data.player }
               console.log(`Player retrieved: ${JSON.stringify(this.player1, null, 2)}`)

            } else if (playerNum == 2) {
               this.player2 = { ...data.player }
               console.log(`Player retrieved: ${JSON.stringify(this.player2, null, 2)}`)
            }

         } catch (err) {
            console.error(`Error retrieving player id ${playerId}: ${err}`)
            alert('Las estadísticas no se han podido cargar')
            this.$router.push({ name:'Face2FaceSelect' })
         }
      },

      selectPlayers() {
         this.$router.push({ name: 'Face2FaceSelect'} ) 
      },
   },

   async mounted() {
      await this.loadPlayer(this.player1Id, 1)
      await this.loadPlayer(this.player2Id, 2)
   }
 }
 </script>

<style></style>