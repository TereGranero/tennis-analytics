<template>
   <div class="mt-4">
      <!-- Loading Message -->
      <div 
         v-if="loading" 
         class="alert alert-info text-responsive-3 text-center"
         role="status"
         aria-live="polite"
         :aria-busy="loading">
         Cargando noticias...
      </div>
      <div 
         v-else-if="error" 
         class="alert alert-info text-responsive-3 text-center"
         role="alert">
         Servicio de noticias no disponible en estos momentos.
      </div>

      <div v-else>
         <div class="row">
            <div v-for="(nw, index) in news" 
               :key="index" 
               class="col-md-6 mb-3">
               <div class="card">
                  <img 
                     v-if="nw.urlToImage"
                     :src="nw.urlToImage" 
                     :alt="`Imagen noticia ${nw.title}`" />
                  <span v-else class="text-center"> Imagen no disponible</span>

                  <div class="card-body">
                     <h4 class="card-title">{{ nw.title }}</h4>
                     <p class="card-text">{{ nw.description }}</p>
                     <a 
                        :href="nw.url" 
                        class="btn btn-submit" 
                        target="_blank">
                        Leer más
                     </a>
                  </div>
               </div>
            </div>
         </div>
      </div>
   </div>
</template>

<script>
import { getSourcesForTennisNews, getTennisNews } from '@/api/newsConnectionService.js'

export default {

   name: 'HomeView',

   props: {
      totalNews: {
         type: Number,
         default: 8
      }
   },

   data() {
      return {
         news: [],
         sources: [],
         loading: true,
         error: false
      }
   },

   methods: {

      async loadSources() {
         try {
            const data = await getSourcesForTennisNews()

            if (data.status == 'error') {
               console.error(`News Api response error: ${data.code}-${data.message}`)
               //alert('Se ha producido un error y no se encontraron fuentes de noticias.')
               this.error = true
            } else {
               console.log(`${data.sources.length} sports news sources have been retrieved.`)
               console.log(data.sources)
               if (data.sources.length == 0) {
                  //alert('No se han encontrado fuentes de noticias.')
                  this.error = true
               } else {
                  this.error = false
                  this.sources = data.sources
                     .slice(0, 20)        // Max 20 sources
                     .map(source => source.id)
                     .join(',')
               }
            }

         } catch(err) {
            console.error(`Error retrieving sources: ${err}`)
            this.error = true
            //alert('Se ha producido un error y no se encontraron fuentes de noticias.')
         }
      },

      async loadNews() {
         try {
            const data = await getTennisNews(this.sources)

            if (data.status == 'error') {
               console.error(`News Api response error: ${data.code}-${data.message}`)
               this.error = true
               //alert('Se ha producido un error y las noticias no se han podido cargar.')
            } else {
               console.log(`${data.totalResults} news have been retrieved.`)
               if (data.totalResults == 0) {
                  //alert('No se han encontrado noticias de tenis.')
                  this.error = true
               } else {
                  this.news = data.articles.slice(0, this.totalNews)
                  this.error = false
               }
            }

         } catch(err) {
            console.error(`Error retrieving news: ${err}`)
            this.error = true
            //alert('Se ha producido un error y las noticias no se han podido cargar.')
         }
      },
   },

   async created() {
      await this.loadSources()
      await this.loadNews()
      this.loading = false
   }
   
}
</script>

<style scoped>
   .card img {
      width: 100%;
      height: auto;
      max-height: 400px;
      object-fit: contain;
   }
   .card-text {
      font-size: 1.1rem;
   }
</style>
