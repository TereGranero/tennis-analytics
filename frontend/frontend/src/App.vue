<template>
   <div>
      <!-- Skip Link by https://vuejs.org/guide/best-practices/accessibility -->
      <span ref="backToTop" tabindex="-1"></span>
         <a 
            href="#content" 
            ref="skipLink" 
            class="visually-hidden-focusable">
            Saltar al contenido principal
         </a> 

      <div class="app m-3 mt-md-4 mt-lg-5">
         <div class="row align-items-center">

            <!-- Logo -->
            <div class="col-12 col-md-8 col-lg-6 col-xl-3 mb-3 mb-xl-0">
               <HeaderImage
                  imgName="logo"
                  alt="Logotipo Tennis Analytics" />
            </div>

            <!-- Navigation menu -->
            <div class="col-12 mb-3 mb-xl-5">
               <nav class="navbar navbar-expand-lg navbar-light bg-white text-responsive-3 ms-3 me-5">

                  <button
                     class="navbar-toggler"
                     type="button"
                     data-bs-toggle="collapse"
                     data-bs-target="#navBarMenu"
                     aria-controls="navbarMenu"
                     aria-expanded="false"
                     aria-label="Toggle navigation">
                     <span class="navbar-toggler-icon"></span>
                  </button>

                  <div class="collapse navbar-collapse" id="navBarMenu">
                     <ul class="navbar-nav ms-auto">
                        <li class="nav-item">
                           <router-link to="/" class="nav-link p-1 p-lg-3">Inicio</router-link>
                        </li>
                        <li class="nav-item">
                           <router-link to="/players" class="nav-link p-1 p-lg-3">Jugadores</router-link>
                        </li>
                        <li class="nav-item">
                           <router-link to="/rankings" class="nav-link p-1 p-lg-3">Rankings</router-link>
                        </li>
                        <li class="nav-item">
                           <router-link to="/tournaments" class="nav-link p-1 p-lg-3">Torneos</router-link>
                        </li>
                        <li class="nav-item">
                           <router-link to="/face2face/select" class="nav-link p-1 p-lg-3">Face2Face</router-link>
                        </li>
                        <li class="nav-item me-5">
                           <router-link to="/login" class="nav-link p-1 p-lg-3">Login</router-link>
                        </li>
                     </ul>
                  </div>
               </nav> 
            </div>
         </div>

         <!-- Main content -->
         <main id="content">
            <router-view />
         </main>
      </div>
   </div>
</template>

<script>
import HeaderImage from './components/HeaderImage.vue'

export default {

   name: 'App',
   components: { HeaderImage }
}
</script>


<style scoped>

</style>
