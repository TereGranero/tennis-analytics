<template>
   <div class="container">

      <!-- Conditional Header Image -->
      <div class="row mb-3">
         <div class="col-12">
            <HeaderImage
               :imgName="imgName"
               :alt="alt" />
         </div>
      </div>

      <form 
         class="row g-3 g-md-5 text-responsive-4"
         @submit.prevent="sendForm">

         <!-- First Name -->
         <div class="col-md-5">
            <label
               for="nameFirstInput"
               class="form-label">
               Nombre: 
            </label>
            <input
               id="nameFirstInput"
               ref="reference"
               type="text" 
               class="form-control"
               :class="{'is-invalid': processing && invalidFirstName}"
               @focus="resetState"
               @keypress="resetState"
               v-model="player.name_first">
            <div v-if="processing && invalidFirstName" class="invalid-feedback">
               Debes rellenar el campo Nombre
            </div>
         </div>

         <!-- Last Name -->
         <div class="col-md-5">
            <label 
               for="nameLastInput" 
               class="form-label">
               Apellido: 
            </label>
            <input 
               id="nameLastInput"
               type="text" 
               class="form-control"
               :class="{'is-invalid': processing && invalidLastName}"
               @focus="resetState"
               v-model="player.name_last">
            <div 
               v-if="processing && invalidLastName" 
               class="invalid-feedback">
               Debes rellenar el campo Apellido
            </div>
         </div>

         <!-- Birth Date -->
         <div class="col-md-5 col-lg-3">
            <label
               for="birthInput"
               class="form-label">
               Fecha de nacimiento:
            </label>
            <input
               id="birthInput"
               type="date" 
               class="form-control"
               :class="{'is-invalid': processing && invalidBirthDate}" 
               @focus="resetState"
               v-model="player.birth_date">
            <div v-if="processing && invalidBirthDate" class="invalid-feedback">
               Debes seleccionar una fecha válida
            </div>
         </div>

         <!-- Country -->
         <div class="col-md-5">
            <label
               for="countrySelect"
               class="form-label">
               País:
            </label>
            <select
               id="countrySelect"
               class="form-select"
               :class="{'is-invalid': processing && invalidCountry}"
               @focus="resetState"
               v-model="player.country">
               <option 
                  v-for="country in allCountries"
                  :key="country.code"
                  :value="country.code"
                  class="text-responsive-5">
                  {{ country.name }}
               </option>
            </select>
            <div 
               v-if="processing && invalidCountry"
               class="invalid-feedback">
               Debes seleccionar un país
            </div>
         </div>

         <!-- Pro Since -->
         <div class="col-md-5 col-lg-3">
            <label
               for="proSinceInput"
               class="form-label text-responsive-4">
               Profesional desde: 
            </label>
            <input 
               id="proSinceInput"
               type="number"
               step="1"
               pattern="\d{1,4}"
               class="form-control"
               :class="{'is-invalid': processing && invalidProSince}"
               @focus="resetState"
               v-model="player.pro_since">
            <div 
               v-if="processing && invalidProSince" 
               class="invalid-feedback">
               Debes proporcionar un año válido
            </div>
         </div>
      
         <!-- Height -->
         <div class="col-md-5 col-lg-3">
            <label
               for="heightInput"
               class="form-label text-responsive-4">
               Altura (cm): 
            </label>
            <input
               id="heightInput"
               type="number"
               step="1"
               pattern="\d{1,3}"
               class="form-control"
               :class="{'is-invalid': processing && invalidHeight}"
               @focus="resetState"
               v-model="player.height">
            <div 
               v-if="processing && invalidHeight" 
               class="invalid-feedback">
               Debes proporcionar una altura válida en centímetros
            </div>
         </div>

         <!-- Weight -->
         <div class="col-md-5 col-lg-3">
            <label
               for="weightInput"
               class="form-label text-responsive-4">
               Peso (Kg): 
            </label>
            <input
               id="weightInput"
               type="number"
               step="1"
               pattern="\d{1,3}"
               class="form-control"
               :class="{'is-invalid': processing && invalidWeight}"
               @focus="resetState"
               v-model="player.weight">
            <div 
               v-if="processing && invalidWeight" 
               class="invalid-feedback">
               Debes proporcionar un peso válido en kilogramos
            </div>
         </div>

         <!-- Hand -->
         <div class="col-md-5 col-lg-3">
            <label
               for="handSelect"
               class="form-label text-responsive-4">
               Mano:
            </label>
            <select
               id="handSelect"
               class="form-select text-responsive-4"
               :class="{'is-invalid': processing && invalidHand}"
               @focus="resetState"
               v-model="player.hand">
               <option 
                  v-for="hand in allHands"
                  :key="hand"
                  :value="hand">
                  {{ hand }}
               </option>
            </select>
            <div 
               v-if="processing && invalidHand" 
               class="invalid-feedback">
               Debes seleccionar la mano con la que juega 
            </div>
         </div>

         <!-- Wikidata ID -->
         <div class="col-md-5 col-lg-2">
            <label
               for="wikidataInput"
               class="form-label">
               Wikidata Id: 
            </label>
            <input 
               type="text" 
               class="form-control"
               @focus="resetState">
         </div>

         <!-- Instagram Username -->
         <div class="col-md-5 col-lg-4">
            <label
               for="instagramInput"
               class="form-label text-responsive-4">
               Instagram: 
            </label>
            <input
               id="instagramInput"
               type="text" 
               class="form-control"
               @focus="resetState"
               v-model="player.instagram">
         </div>

         <!-- Facebook Username -->
         <div class="col-md-5 col-lg-4">
            <label
               for="facebookInput"
               class="form-label text-responsive-4">
               Facebook:
            </label>
            <input
               id="facebookInput"
               type="text" 
               class="form-control"
               @focus="resetState"
               v-model="player.facebook">
         </div>

         <!-- X-Twitter Username -->
         <div class="col-md-5 col-lg-4">
            <label
               for="xInput"
               class="form-label text-responsive-4">
               X-Twitter: 
            </label>
            <input
               id="xInput"
               type="text" 
               class="form-control"
               @focus="resetState"
               v-model="player.x_twitter">
         </div>

         <!-- Buttons -->
         <div class="d-flex flex-wrap gap-5 justify-content-center mt-3 mt-md-5">
            <div class="form-group">
               <button 
                  type="submit"
                  class="btn btn-secondary me-3">
                  Aceptar
               </button>
               <button 
                  type="button"
                  class="btn btn-outline-secondary" 
                  @click="cancelForm">
                  Cancelar
               </button>
            </div>
         </div>
      </form>
   </div>
</template>

<script>
import countries from 'i18n-iso-countries'
import es from 'i18n-iso-countries/langs/es.json'
import { getPlayerByIdForEditing } from '@/api/serverConnectionService.js'
import { normalizeIntoBackend, normalizeIntoForm } from '@/services/normalization_services'
import HeaderImage from '../HeaderImage.vue'

export default {

   name: 'PlayerForm',

   components: { HeaderImage },

   props: {
      id: {
         type: String,
         default: null,
      }
   },

   data() {
      return {
         player: {
            player_id: '',
            name_first: '',
            name_last: '',
            hand: '-',
            birth_date: null,
            country: '-',
            height: 0,
            wikidata_id: '',
            fullname: '',
            weight: 0,
            instagram: '',
            facebook: '',
            x_twitter: '',
            pro_since: 2000
         },
         allCountries: [],  // comes from library
         allHands: ['-', 'Derecha', 'Izquierda'],
         processing: false,
         error: false,
         imgName: '',
         alt: ''
      }
   },

   computed: {
      isEditing() {
         console.log(`Checking if there is an id for editing: ${this.id}`)
         return this.id !== null
      },

      formattedFirstName() {
         // Checks if fistName is already formatted as initials
         const isFormatted = this.player.name_first
            .split(' ')
            .every(word => /^[A-Z](\.[A-Z])*\.$/.test(word))

         if (isFormatted) {
            return this.player.name_first
         }
         // Formats as initials
         return this.player.name_first
            .split(' ')
            .map((word) => word.charAt(0).toUpperCase() + '.')
            .join('')
      },

      // --------------------------- Validates Form ---------------------------
      
      invalidLastName() {
         // 2 chars o more
         return this.player.name_last < 2
      },

      invalidFirstName() {
         // 1 char or more
         return this.player.name_first < 1
      },

      invalidBirthDate() {
         // not future dates
         if (this.player.birth_date){
            return ( new Date(this.player.birth_date) > new Date() ) 
         }
         return false
      },
      
      invalidProSince() {
         // allowed years 1800-current_year
         if (this.player.pro_since){
            return (      
               this.player.pro_since != 0 &&
               (this.player.pro_since < 1800 || 
               this.player.pro_since > new Date().getFullYear()) 
            ) 
         }
         return false
      },

      invalidCountry() {
         // choose one from select
         return (
            !this.player.country || 
            this.player.country == '-'
         )
      },

      invalidHeight() {
         // allowed values 100-270
         return (
            this.player.height != 0 &&
            (this.player.height < 100 || 
            this.player.height > 270)
         )
      },

      invalidWeight() {
         // allowed values 45-150
         return (
            this.player.weight != 0 &&
            (this.player.weight < 45 || 
            this.player.weight > 150)
         )
      },
            
      invalidHand() {
         // no restrictions for now
         return ( 
            !this.player.hand // || this.player.hand == '-'
         )
      },
   },

   watch: {
      // Launches method updateFullname when name_last or name_first is updated
      'player.name_last': 'updateFullname',
      'player.name_first': 'updateFullname',
   },

   methods: {
      initCountries() {
         countries.registerLocale(es)
         // countries.getNames('es') -> object code:name
         // Object.entries -> array of [code, name]
         // .map(([code, name]) --> array de objetos { code: "ES", name: "España" }
         this.allCountries = Object.entries(countries.getNames('es')).map(([code, name]) => ({
            code,
            name,
         })).sort((a, b) => a.name.localeCompare(b.name))
      },

      generatePlayerId() {
         return 'A' + (Math.floor(Math.random()*10000000)).toString()
      },

      updateFullname() {
         this.player.fullname = `${this.player.name_last} ${this.formattedFirstName}`
      },

      sendForm() {
         this.processing = true
         this.resetState()

         // Validates fields
         if(this.invalidLastName || 
            this.invalidFirstName ||
            this.invalidBirthDate ||
            this.invalidCountry || 
            this.invalidHeight || 
            this.invalidWeight || 
            this.invalidProSince ||
            this.invalidHand) {
               this.error = true
               return
         }

         // Normalizes into backend
         this.player = normalizeIntoBackend(this.player)

         // Sends events
         if (this.isEditing) {
            console.log(`Player updated to: ${JSON.stringify(this.player, null, 2)}`) // 2spaces identation 
            this.$emit('edit-player', this.player.player_id, this.player)

         } else {
            // Assigns new player_id
            this.player.player_id = this.generatePlayerId()

            console.log(`New player is: ${JSON.stringify(this.player, null, 2)}`)
            this.$emit('add-player', this.player)
         }

         // Resets form and variables
         this.player = {
            player_id: '',
            name_first: '',
            name_last: '',
            hand: '-',
            birth_date: null,
            country: '-',
            height: 0,
            wikidata_id: '',
            fullname: '',
            weight: 0,
            instagram: '',
            facebook: '',
            x_twitter: '',
            pro_since: 2000
         },
         this.processing = false
         this.error = false
      },
      
      resetState(){
         this.error = false
      },

      cancelForm(){
         this.$router.push('/players')
      },
   },

   async mounted() {
      if (this.isEditing) {

         this.imgName = 'editplayer-banner'
         this.alt = 'Título editar jugador'
         
         console.log(`Editing player id: ${this.id}`)
         const data = await getPlayerByIdForEditing(this.id)

         if (data.status == 'error') {
            console.error(`Backend response error: ${data.message}`)

         } else {
            let player_retrieved = { ...data.player }
            console.log(`Player retrieved: ${JSON.stringify(player_retrieved , null, 2)}`)

            // Normalizes into Form
            this.player = normalizeIntoForm(player_retrieved )
         }
      } else {
         this.imgName = 'addplayer-banner'
         this.alt = 'Título añadir jugador'
      }

      this.initCountries()
   }
}
</script>

<style scoped>
   form {
      margin-bottom: 2rem;
   }
</style>