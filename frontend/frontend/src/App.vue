<template>
   <div class="d-flex flex-column min-vh-100">
      <!-- Skip Link by https://vuejs.org/guide/best-practices/accessibility -->
      <span ref="backToTop" tabindex="-1"></span>
         <a 
            href="#mainContent" 
            ref="skipLink" 
            class="visually-hidden">
            Saltar al contenido principal
         </a> 

      <div class="row align-items-center m-3">

         <!-- Logo -->
         <div class="col-12 col-md-8 col-lg-6 col-xl-3">
            <HeaderImage2
               imgName="logo-minimalist"
               alt="Logotipo Tennis Analytics" />
         </div>

         <!-- Main menu -->
         <div class="col-12 mb-3 mb-xl-5">
            <nav 
               class="navbar navbar-expand-lg navbar-light bg-transparent text-responsive-4 ms-3 me-5 mb-3"
               role="navigation">

               <button
                  class="navbar-toggler ms-sm-5"
                  type="button"
                  data-bs-toggle="collapse"
                  data-bs-target="#navBarMenu"
                  aria-controls="navBarMenu"
                  aria-expanded="false"
                  aria-label="Abrir y cerrar el menú principal">
                  <span class="navbar-toggler-icon"></span>
               </button>

               <div class="collapse navbar-collapse" id="navBarMenu">
                  <ul class="navbar-nav ms-auto">
                     <li class="nav-item">
                        <router-link 
                           to="/" 
                           class="nav-link p-1 p-lg-3"
                           active-class="active">
                           Inicio
                        </router-link>
                     </li>
                     <li class="nav-item">
                        <router-link 
                           to="/players" 
                           class="nav-link p-1 p-lg-3"
                           active-class="active">
                           Jugadores
                        </router-link>
                     </li>
                     <li class="nav-item">
                        <router-link 
                           to="/rankings" 
                           class="nav-link p-1 p-lg-3"
                           active-class="active">
                           Rankings
                        </router-link>
                     </li>
                     <li class="nav-item">
                        <router-link 
                           to="/tournaments" 
                           class="nav-link p-1 p-lg-3"
                           active-class="active">
                           Torneos
                        </router-link>
                     </li>
                     <li class="nav-item">
                        <router-link 
                           to="/face2face/select" 
                           class="nav-link p-1 p-lg-3"
                           active-class="active">
                           Face2Face
                        </router-link>
                     </li>
                     <li class="nav-item me-5">
                        <router-link 
                           to="/login" 
                           class="nav-link p-1 p-lg-3"
                           active-class="active">
                           Login
                        </router-link>
                     </li>
                  </ul>
               </div>
            </nav> 
         </div>
      </div>

      <!-- Main content -->
       <div 
         id="mainContent"
         class="flex-grow-1 mb-5">
         <router-view />
      </div>

      <!-- Footer with credits -->
      <footer class="mt-auto">
         <p>Aplicación web creada por Teresa Granero como proyecto fin de ciclo DAW (2025).</p>
         <p>Origen de los datos: Kaggle <a 
            href="https://www.kaggle.com/datasets/guillemservera/tennis">
            Huge Tennis Dataset
            </a> por guillemservera, basado en el trabajo original de <a 
            href="https://github.com/JeffSackmann/tennis_atp" >
            Jeff Sackmann 
            </a>, bajo licencia: <a 
            href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
            Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
            </a>
         </p>
         <p>Datos enriquecidos con  <a 
            href="https://www.wikidata.org">
            Wikidata.
            </a> 
         </p>
      </footer>

   </div>
</template>

<script>
import HeaderImage2 from './components/HeaderImage2.vue'
export default {

   name: 'App',

   components: { HeaderImage2 }

}
</script>

<style scoped>
   footer {
      background-color: #013a29; 
      color: white; 
      text-align: center; 
      padding: 1em;
   }

   footer a {
      color: white; 
      text-decoration: underline;
   }
</style>
