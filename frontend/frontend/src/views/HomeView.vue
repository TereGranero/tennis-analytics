<template>
   <div class="container mt-4">
      <h2 class="text-center">Últimas noticias de tenis</h2>
      <div v-if="loading" class="text-center">
         Cargando noticias...
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
                     alt="Imagen noticia" />
                  <span v-else class="text-center"> Imagen no disponible</span>

                  <div class="card-body">
                     <h4 class="card-title">{{ nw.title }}</h4>
                     <p class="card-text">{{ nw.description }}</p>
                     <a 
                        :href="nw.url" 
                        class="btn btn-secondary" 
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

   data() {
      return {
         news: [],
         sources: [],
         loading: true
      }
   },

   methods: {

      async loadSources() {
         try {
            const data = await getSourcesForTennisNews()

            if (data.status == 'error') {
               console.error(`News Api response error: ${data.code}-${data.message}`)
               alert('Se ha producido un error y no se encontraron fuentes de noticias.')
            } else {
               console.log(`${data.sources.length} sports news sources have been retrieved.`)
               if (data.sources.length == 0) {
                  alert('No se han encontrado fuentes de noticias.')
               }
               
               this.sources = data.sources
                  .slice(0, 20)        // Max 20 sources
                  .map(source => source.id)
                  .join(',')
            }

         } catch(err) {
            console.error(`Error retrieving sources: ${err}`)
            alert('Se ha producido un error y no se encontraron fuentes de noticias.')
         }
      },

      async loadNews() {
         try {
            const data = await getTennisNews(this.sources)

            if (data.status == 'error') {
               console.error(`News Api response error: ${data.code}-${data.message}`)
               alert('Se ha producido un error y las noticias no se han podido cargar.')
            } else {
               console.log(`${data.totalResults} news have been retrieved.`)
               if (data.totalResults == 0) {
                  alert('No se han encontrado noticias de tenis.')
               }
               this.news = data.articles.slice(0, 8)
            }

         } catch(err) {
            console.error(`Error retrieving news: ${err}`)
            alert('Se ha producido un error y las noticias no se han podido cargar.')
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
