<template>
   <main class="container">

      <!-- Heading -->
      <h1 
         id="face2faceShowHeading" 
         class="text-green text-center text-responsive-1 mb-5">
         Face2Face
      </h1>

      <!-- Select Button -->
      <section   
         class="row text-center text-md-end align-items-center mb-3 mb-sm-4 mb-md-5" 
         aria-labelledby="selectHeading"
         v-if="player1 && player2">

         <h2 
            id="selectHeading" 
            class="visually-hidden">
            Seleccionar otros jugadores para comparar
         </h2>
         <div class="col-12 mb-3 col-md-auto mb-md-0">
            <button 
               type="button" 
               class="btn btn-outline-dark btn-lg" 
               @click="selectPlayers"
               aria-labelledby="selectHeading">
               Seleccionar jugadores
            </button>
         </div>
      </section>

      <!-- Players Headers -->
      <section 
         class="row justify-content-center align-items-start mb-5"
         aria-labelledby="playersHeading">

         <h2 
            id="playersHeading" 
            class="visually-hidden">
            Comparación de jugadores
         </h2>

         <!-- Player 1 -->
         <article
            v-if="player1"
            class="col-12 col-md-6 d-flex flex-column"
            aria-labelledby="player1Heading">

            <!-- Header fullname and flag -->
            <PlayerFullnameFlagHeader
               :player="player1"
               id="player1Heading"/>
            
            <!-- Player photo -->
            <div class="d-flex justify-content-center">
               <button 
                  class="btn btn-link text-decoration-none p-0 border-0"
                  @click="viewPlayer(player1.player_id)"
                  :aria-label="`Ver ficha de ${player1.fullname}`">
                  <PlayerPhotoByWikidataId
                     :playerWikidataId="player1.wikidata_id"
                     :setHeight="true"/>
               </button>
            </div>
         </article>

         <div v-else 
            class="col-12 col-md-6">
            <div 
               class="alert alert-info text-responsive-3 text-center"
               role="status"
               aria-live="polite"
               :aria-busy="!player1">
               Cargando jugador 1...
            </div>
         </div>


         <!-- Player 2 -->
         <article
            v-if="player2"
            class="col-12 col-md-6 d-flex flex-column"
            aria-labelledby="player2Heading">

            <!-- Header fullname and flag -->
            <PlayerFullnameFlagHeader
               :player="player2"
               id="player2Heading"/>

            <!-- Player photo -->
            <div class="d-flex justify-content-center">
               <button 
                  class="btn btn-link text-decoration-none p-0 border-0"
                  @click="viewPlayer(player2.player_id)"
                  :aria-label="`Ver ficha de ${player2.fullname}`">
                  <PlayerPhotoByWikidataId
                     :playerWikidataId="player2.wikidata_id"
                     :setHeight="true"/>
               </button>
            </div>
         </article>

         <div v-else 
            class="col-12 col-md-6">
            <div 
               class="alert alert-info text-responsive-3 text-center"
               role="status"
               aria-live="polite"
               :aria-busy="!player2">
               Cargando jugador 2...
            </div>
         </div>         
      </section>

      <!-- KPIs comparison -->
      <section
         v-if="player1 && player2"
         aria-labelledby="comparisonHeading"
         class="row justify-content-center align-items-start mb-5 mx-mb-3">

         <h2 
            id="comparisonHeading" 
            class="visually-hidden">
            Comparación de estadísticas
         </h2>
         <div class="col-12 col-md-6 d-flex flex-column">
            <div 
               role="group"
               aria-labelledby="comparisonHeading">
               
               <Face2FaceDoubleKpi
                  v-for="kpi in kpiData" 
                  :key="kpi.title" 
                  :title="kpi.title"
                  :value1="kpi.value1"
                  :value2="kpi.value2"
                  :percentage="kpi.percentage"
                  class="mb-3"/>
            </div>
         </div>
      </section>
   </main>
 </template>
 
<script>
import PlayerPhotoByWikidataId from '@/components/players/PlayerPhotoByWikidataId.vue'
import PlayerFullnameFlagHeader from '@/components/players/PlayerFullnameFlagHeader.vue'
import Face2FaceDoubleKpi from '@/components/face2face/Face2FaceDoubleKpi.vue'
import { getPlayerById } from '@/api/serverConnectionService.js'

export default {

   name: 'Face2FaceShowView',

   components: { 
      PlayerPhotoByWikidataId,
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
         alt: 'Título Face2Face'
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
               value2: this.player2.best_ranking || '-',
               percentage: false
            },
            {
               title: 'Títulos',
               value1: this.player1.total_titles  || '-',
               value2: this.player2.total_titles  || '-',
               percentage: false
            },
            {
               title: 'Grand Slams',
               value1: this.player1.grand_slams  || '0',
               value2: this.player2.grand_slams  || '0',
               percentage: false
            },
            {
               title: 'Masters 1000',
               value1: this.player1.masters1000  || '0',
               value2: this.player2.masters1000  || '0',
               percentage: false
            },
            {
               title: 'W/L Ratio',
               value1: this.player1.w_l  || '-',
               value2: this.player2.w_l  || '-',
               percentage: false
            },
            {
               title: 'Aces',
               value1: this.player1.aces  || '-',
               value2: this.player2.aces  || '-',
               percentage: false
            },
            {
               title: 'Aces por partido',
               value1: this.player1.aces_match  || '-',
               value2: this.player2.aces_match  || '-',
               percentage: false
            },
            {
               title: 'Dobles Faltas',
               value1: this.player1.double_faults  || '-',
               value2: this.player2.double_faults  || '-',
               percentage: false
            },
            {
               title: 'Dobles Faltas por partido',
               value1: this.player1.double_faults_match  || '-',
               value2: this.player2.double_faults_match  || '-',
               percentage: false
            },
            {
               title: 'Puntos ganados con 1er servicio',
               value1: this.player1.points_on_first  || '-',
               value2: this.player2.points_on_first  || '-',
               percentage: false
            },
            {
               title: 'Puntos con 1er servicio por partido',
               value1: this.player1.points_on_first_match  || '-',
               value2: this.player2.points_on_first_match  || '-',
               percentage: false
            },
            {
               title: 'Juegos ganados al saque',
               value1: this.player1.games_on_serve  || '-',
               value2: this.player2.games_on_serve  || '-',
               percentage: false
            },
            {
               title: 'Juegos al saque por partido',
               value1: this.player1.games_on_serve_match  || '-',
               value2: this.player2.games_on_serve_match  || '-',
               percentage: false
            },
            {
               title: '1er servicio dentro',
               value1: this.player1.first_in  || '-',
               value2: this.player2.first_in  || '-',
               percentage: false
            },
            {
               title: '1er servicio dentro por partido',
               value1: this.player1.first_in_match  || '-',
               value2: this.player2.first_in_match  || '-',
               percentage: false
            },
            {
               title: 'Puntos de rotura encarados',
               value1: this.player1.bp_faced  || '-',
               value2: this.player2.bp_faced  || '-',
               percentage: false
            },
            {
               title: 'Puntos de rotura salvados',
               value1: this.player1.bp_saved_percentage || '-',
               value2: this.player2.bp_saved_percentage || '-',
               percentage: true
            },
         ]
      },
   },

   /* https://vuejs.org/guide/best-practices/accessibility
   following https://www.w3.org/WAI/WCAG21/Techniques/general/G1.html
   */
   watch: {
      $route() {
         this.$refs.backToTop.focus()
      }
   },

   methods: {

      async loadPlayer(playerId, playerNum) {
         try {
            const data = await getPlayerById(playerId)

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

      viewPlayer(id) {
         console.log(`Face2faceShowView sends id ${id} to PlayerView` )
         this.$router.push({ name: 'Player', params: { id } })
      },
   },

   async mounted() {
      await this.loadPlayer(this.player1Id, 1)
      await this.loadPlayer(this.player2Id, 2)
   }
 }
 </script>

<style></style>