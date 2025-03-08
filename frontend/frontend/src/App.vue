<template>
   <div class="app">
      <div class="row align-items-center m-3 mt-md-5 mt-lg-8">

         <!-- Logo -->
         <div class="col-12 col-sm-12 col-md-7 col-lg-5 col-xl-3">
            <HeaderImage
               imgName="logo"
               alt="Logo" />
         </div>

         <!-- Navigation menu -->
         <div class="col-12 col-sm-12 col-md-5 col-lg-7 col-xl-9">
            <nav class="navbar navbar-expand-md navbar-light bg-white">

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


<style>
  #app {
    margin: 10px;
  }

  li {
    font-size: 1.4rem;
  }
</style>
