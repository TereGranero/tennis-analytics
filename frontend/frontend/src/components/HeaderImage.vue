<template>
   <picture>
      <!-- Mobile -->
      <source :srcset="imgPathMobile" media="(max-width: 768px)">

      <!-- Tablet -->
      <source :srcset="imgPathTablet" media="(max-width: 1024px)">
      
      <!-- Large screen -->
      <img 
         :src="imgPath" 
         :alt="altText" 
         class="img-fluid w-100"/>
   </picture>
</template>

<script>
export default {

   name: 'HeaderImage',

   props: {
      imgName: {
         type: String,
         required: true
      },

      alt: {
         type: String,
         default: 'Imagen'
      }
   },

   data() {
      return {
         imagesPath: '/images',
      }
   },

   computed: {
      imgPath() {
         return `${this.imagesPath}/${this.imgName.toLowerCase()}.png`
      },

      imgPathTablet() {
         return `${this.imagesPath}/${this.imgName.toLowerCase()}-tablet.png`
      },

      imgPathMobile() {
         return `${this.imagesPath}/${this.imgName.toLowerCase()}-mobile.png`
      },

      altText() {
         return `Imagen ${this.alt}`
      }
   }
}
</script>

<style></style>