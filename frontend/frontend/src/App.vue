<template>
   <div class="app m-3 mt-md-4 mt-lg-5">
      <div class="row align-items-center">

         <!-- Logo -->
         <div class="col-12 col-sm-12 col-md-7 col-lg-5 col-xl-3 mb-sm-3 mb-md-5">
            <HeaderImage
               imgName="logo"
               alt="Logo" />
         </div>

         <!-- Navigation menu -->
         <div class="col-12 col-sm-12 col-md-5 col-lg-7 col-xl-9">
            <nav class="navbar navbar-expand-md navbar-light bg-white text-responsive-3">

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
                        <router-link to="/players" class="nav-link p-2 p-lg-3">Jugadores</router-link>
                     </li>
                     <li class="nav-item">
                        <router-link to="/rankings" class="nav-link p-2 p-lg-3">Rankings</router-link>
                     </li>
                     <li class="nav-item">
                        <router-link to="/tournaments" class="nav-link p-2 p-lg-3">Torneos</router-link>
                     </li>
                  </ul>
               </div>
            </nav> 
         </div>
      </div>

      <router-view />
   </div>
</template>

<script>
import HeaderImage from './components/HeaderImage.vue'

export default {
   name: 'App',
   components: { HeaderImage }
}
</script>


<style></style>
