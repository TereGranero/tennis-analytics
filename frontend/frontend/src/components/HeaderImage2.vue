<template>
   <picture>
      <img 
         :src="imgPath" 
         :alt="altText" 
         class="img-fluid w-100"/>
   </picture>
</template>

<script>
export default {

   name: 'HeaderImage2',

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

      altText() {
         return this.alt
      }
   }
}
</script>

<style></style>