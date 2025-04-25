<template>
   <main class="container mb-5">

      <!-- Conditional Heading -->
      <h1 
         id="formHeading" 
         class="text-center text-green text-responsive-1 mb-5">
         {{ title }}
      </h1>


      <!-- Player Form -->
      <form 
         class="row g-3 g-md-5 mb-5 text-responsive-5"
         @submit.prevent="sendForm">

         <!-- First Name -->
         <div 
            class="col-md-5"
            role="group" 
            aria-labelledby="nameFirstLabel">
            <label
               id="nameFirstLabel"
               for="nameFirstInput"
               class="form-label">
               Nombre: 
            </label>
            <input
               id="nameFirstInput"
               ref="reference"
               type="text" 
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               :class="{'is-invalid': processing && invalidFirstName}"
               @focus="resetState"
               @keypress="resetState"
               v-model="player.name_first"
               aria-required="true"   
               :aria-invalid="processing && invalidFirstName"
               aria-describedby="nameFirstError">
            <div 
               v-if="processing && invalidFirstName" 
               id="nameFirstError"
               class="invalid-feedback"
               role="alert">
               Por favor, rellena el campo Nombre
            </div>
         </div>

         <!-- Last Name -->
         <div 
            class="col-md-5"
            role="group" 
            aria-labelledby="nameLastLabel">
            <label 
               id="nameLastLabel"
               for="nameLastInput" 
               class="form-label">
               Apellido: 
            </label>
            <input 
               id="nameLastInput"
               type="text" 
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               :class="{'is-invalid': processing && invalidLastName}"
               @focus="resetState"
               v-model="player.name_last"
               aria-required="true"   
               :aria-invalid="processing && invalidLastName"
               aria-describedby="nameLastError">
            <div 
               v-if="processing && invalidLastName"
               id="nameLastError"
               class="invalid-feedback"
               role="alert">
               Por favor, rellena el campo Apellido.
            </div>
         </div>

         <!-- Birth Date -->
         <div 
            class="col-md-5 col-lg-3"
            role="group" 
            aria-labelledby="birthDateLabel">
            <label
               id="birthDateLabel"
               for="birthInput"
               class="form-label">
               Fecha de nacimiento:
            </label>
            <input
               id="birthInput"
               type="date" 
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               :class="{'is-invalid': processing && invalidBirthDate}" 
               @focus="resetState"
               v-model="player.birth_date"
               :aria-invalid="processing && invalidBirthDate"
               aria-describedby="birthDateError">
            <div 
               v-if="processing && invalidBirthDate" 
               id="birthDateError"
               class="invalid-feedback"
               role="alert">
               Por favor, selecciona una fecha válida.
            </div>
         </div>

         <!-- Country -->
         <div 
            class="col-md-5"
            role="group" 
            aria-labelledby="countryLabel">
            <label
               id="countryLabel"
               for="countrySelect"
               class="form-label">
               País:
            </label>
            <select
               id="countrySelect"
               class="form-select border-dark bg-transparent text-dark text-responsive-4"
               :class="{'is-invalid': processing && invalidCountry}"
               @focus="resetState"
               v-model="player.country"
               :aria-invalid="processing && invalidCountry"
               aria-describedby="countryError">
               <option 
                  v-for="country in allCountries"
                  :key="country.code"
                  :value="country.code">
                  {{ country.name }}
               </option>
            </select>
            <div 
               v-if="processing && invalidCountry"
               id="countryError"
               class="invalid-feedback"
               role="alert">
               Por favor, selecciona un país del listado.
            </div>
         </div>

         <!-- Pro Since -->
         <div 
            class="col-md-5 col-lg-3"
            role="group" 
            aria-labelledby="proSinceLabel">
            <label
               id="proSinceLabel"
               for="proSinceInput"
               class="form-label">
               Profesional desde: 
            </label>
            <input 
               id="proSinceInput"
               type="number"
               step="1"
               pattern="\d{1,4}"
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               :class="{'is-invalid': processing && invalidProSince}"
               @focus="resetState"
               v-model="player.pro_since"
               :aria-invalid="processing && invalidProSince"
               aria-describedby="proSinceError">
            <div 
               v-if="processing && invalidProSince" 
               id="proSinceError"
               class="invalid-feedback"
               role="alert">
               Por favor, escribe un año válido.
            </div>
         </div>
      
         <!-- Height -->
         <div 
            class="col-md-5 col-lg-3"
            role="group" 
            aria-labelledby="heightLabel">
            <label
               id="heightLabel"
               for="heightInput"
               class="form-label">
               Altura (cm): 
            </label>
            <input
               id="heightInput"
               type="number"
               step="1"
               pattern="\d{1,3}"
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               :class="{'is-invalid': processing && invalidHeight}"
               @focus="resetState"
               v-model="player.height"
               :aria-invalid="processing && invalidHeight"
               aria-describedby="heightError">
            <div 
               v-if="processing && invalidHeight" 
               id="heightError"
               class="invalid-feedback"
               role="alert">
               Por favor, escribe una altura válida en centímetros. Valores permitidos: [100-270]
            </div>
         </div>

         <!-- Weight -->
         <div 
            class="col-md-5 col-lg-3"
            role="group" 
            aria-labelledby="weightLabel">
            <label
               id="weightLabel"
               for="weightInput"
               class="form-label">
               Peso (Kg): 
            </label>
            <input
               id="weightInput"
               type="number"
               step="1"
               pattern="\d{1,3}"
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               :class="{'is-invalid': processing && invalidWeight}"
               @focus="resetState"
               v-model="player.weight"
               :aria-invalid="processing && invalidWeight"
               aria-describedby="weightError">
            <div 
               v-if="processing && invalidWeight"
               id="weightError"
               class="invalid-feedback"
               role="alert">
               Por favor, escribe un peso válido en kilogramos. Valores permitidos: [45-150]
            </div>
         </div>

         <!-- Hand -->
         <div 
            class="col-md-5 col-lg-3"
            role="group" 
            aria-labelledby="handLabel">
            <label
               id="handLabel"
               for="handSelect"
               class="form-label">
               Mano:
            </label>
            <select
               id="handSelect"
               class="form-select border-dark bg-transparent text-dark text-responsive-4"
               :class="{'is-invalid': processing && invalidHand}"
               @focus="resetState"
               v-model="player.hand"
               :aria-invalid="processing && invalidHand"
               aria-describedby="handError">
               <option 
                  v-for="hand in allHands"
                  :key="hand"
                  :value="hand">
                  {{ hand }}
               </option>
            </select>
            <div 
               v-if="processing && invalidHand" 
               id="handError"
               class="invalid-feedback"
               role="alert">
               Por favor, selecciona en la lista la mano con la que juega 
            </div>
         </div>

         <!-- Wikidata ID -->
         <div 
            class="col-md-5 col-lg-2"
            role="group" 
            aria-labelledby="wikidataLabel">
            <label
               id="wikidataLabel"
               for="wikidataInput"
               class="form-label">
               Wikidata Id: 
            </label>
            <input 
               type="text" 
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               @focus="resetState"
               v-model="player.wikidata_id">
               
         </div>

         <!-- Instagram Username -->
         <div 
            class="col-md-5 col-lg-4"
            role="group" 
            aria-labelledby="instagramLabel">
            <label
               id="instagramLabel"
               for="instagramInput"
               class="form-label">
               Instagram: 
            </label>
            <input
               id="instagramInput"
               type="text" 
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               @focus="resetState"
               v-model="player.instagram">
         </div>

         <!-- Facebook Username -->
         <div 
            class="col-md-5 col-lg-4"
            role="group" 
            aria-labelledby="facebookLabel">
            <label
               id="facebookLabel"
               for="facebookInput"
               class="form-label">
               Facebook:
            </label>
            <input
               id="facebookInput"
               type="text" 
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               @focus="resetState"
               v-model="player.facebook">
         </div>

         <!-- X-Twitter Username -->
         <div 
            class="col-md-5 col-lg-4"
            role="group" 
            aria-labelledby="twitterLabel">
            <label
               id="twitterLabel"
               for="xInput"
               class="form-label">
               X-Twitter: 
            </label>
            <input
               id="xInput"
               type="text" 
               class="form-control border-dark bg-transparent text-dark text-responsive-4"
               @focus="resetState"
               v-model="player.x_twitter">
         </div>

         <!-- Buttons -->
         <div 
            class="d-flex flex-wrap gap-5 justify-content-center mt-3 mt-md-5"
            role="group">
            <div class="form-group">
               <button 
                  type="submit"
                  class="btn btn-submit btn-lg me-3">
                  Aceptar
               </button>
               <button 
                  type="button"
                  class="btn btn-cancel btn-lg " 
                  @click="cancelForm">
                  Cancelar
               </button>
            </div>
         </div>
      </form>
   </main>
</template>

<script>
import countries from 'i18n-iso-countries'
import es from 'i18n-iso-countries/langs/es.json'
import { getPlayerByIdForEditing } from '@/api/serverConnectionService.js'
import { normalizeIntoBackend, normalizeIntoForm } from '@/services/normalization_services'

export default {

   name: 'PlayerForm',

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
         title: ''
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

         this.title = 'editar jugador'
         
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
         this.title = 'añadir jugador'
      }

      this.initCountries()
   }
}
</script>

<style></style>