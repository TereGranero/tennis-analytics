<template>
   <div>
      <!-- Conditional title -->
      <h2>{{ isEditing ? 'Modificar Jugador' : 'Añadir Jugador' }}</h2>

      <form @submit.prevent="sendForm">
         <div class="container">

            <!-- Last Name -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>Apellido: </label>
                     <input 
                        ref="reference"
                        type="text" 
                        class="form-control"
                        :class="{'is-invalid': processing && invalidLastName}"
                        @focus="resetState"
                        @keypress="resetState"
                        v-model="player.name_last">
                     <div v-if="processing && invalidLastName" class="invalid-feedback">
                        Debes rellenar el campo Apellido
                     </div>
                  </div>
               </div>
            </div>
         
            <!-- First Name -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>Nombre: </label>
                     <input 
                        type="text" 
                        class="form-control"
                        :class="{'is-invalid': processing && invalidFirstName}"
                        @focus="resetState"
                        v-model="player.name_first">
                     <div v-if="processing && invalidFirstName" class="invalid-feedback">
                        Debes rellenar el campo Nombre
                     </div>
                  </div>
               </div>
            </div>

            <!-- Birth Date -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>Fecha de nacimiento:</label>
                     <input 
                        type="date" 
                        class="form-control"
                        :class="{'is-invalid': processing && invalidBirthDate}" 
                        @focus="resetState"
                        v-model="player.birth_date">
                     <div v-if="processing && invalidBirthDate" class="invalid-feedback">
                        Debes seleccionar una fecha válida
                     </div>
                  </div>
               </div>
            </div>

            <!-- Country -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>País:</label>
                     <select
                        class="form-control"
                        :class="{'is-invalid': processing && invalidCountry}"
                        @focus="resetState"
                        v-model="player.country">
                        <option 
                           v-for="country in allCountries"
                           :key="country.code"
                           :value="country.code">
                           {{ country.name }}
                        </option>
                     </select>
                     <div v-if="processing && invalidCountry" class="invalid-feedback">
                        Debes seleccionar un país
                     </div>
                  </div>
               </div>
            </div>

            <!-- Pro Since -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>Profesional desde el año: </label>
                     <input 
                        type="number"
                        step="1"
                        pattern="\d{1,4}"
                        class="form-control"
                        :class="{'is-invalid': processing && invalidProSince}"
                        @focus="resetState"
                        v-model="player.pro_since">
                     <div v-if="processing && invalidProSince" class="invalid-feedback">
                        Debes proporcionar un año válido
                     </div>
                  </div>
               </div>
            </div>
         
            <!-- Height -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>Altura (cm): </label>
                     <input 
                        type="number"
                        step="1"
                        pattern="\d{1,3}"
                        class="form-control"
                        :class="{'is-invalid': processing && invalidHeight}"
                        @focus="resetState"
                        v-model="player.height">
                     <div v-if="processing && invalidHeight" class="invalid-feedback">
                        Debes proporcionar una altura válida en centímetros
                     </div>
                  </div>
               </div>
            </div>

            <!-- Weight -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>Peso (Kg): </label>
                     <input 
                        type="number"
                        step="1"
                        pattern="\d{1,3}"
                        class="form-control"
                        :class="{'is-invalid': processing && invalidWeight}"
                        @focus="resetState"
                        v-model="player.weight">
                     <div v-if="processing && invalidWeight" class="invalid-feedback">
                        Debes proporcionar un peso válido en kilogramos
                     </div>
                  </div>
               </div>
            </div>

            <!-- Hand -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>Mano:</label>
                     <select
                        class="form-control"
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
                     <div v-if="processing && invalidHand" class="invalid-feedback">
                        Debes seleccionar la mano con la que juega 
                     </div>
                  </div>
               </div>
            </div>

            <!-- Wikidata ID -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>Wikidata Id: </label>
                     <input 
                        type="text" 
                        class="form-control"
                        @focus="resetState"
                        v-model="player.wikidata_id">
                  </div>
               </div>
            </div>

            <!-- Instagram Username -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>Instagram: </label>
                     <input 
                        type="text" 
                        class="form-control"
                        @focus="resetState"
                        v-model="player.instagram">
                  </div>
               </div>
            </div>

            <!-- Facebook Username -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>Facebook: </label>
                     <input 
                        type="text" 
                        class="form-control"
                        @focus="resetState"
                        v-model="player.facebook">
                  </div>
               </div>
            </div>

            <!-- X-Twitter Username -->
            <div class="row justify-content-center">
               <div class="col-md-6">
                  <div class="form-group">
                     <label>X-Twitter: </label>
                     <input 
                        type="text" 
                        class="form-control"
                        @focus="resetState"
                        v-model="player.x_twitter">
                  </div>
               </div>
            </div>

            <!-- Buttons -->
            <div class="row">
               <div class="col-md-12">
                  <div class="form-group">
                  <button type="submit" class="btn btn-secondary">Aceptar</button>
                  <button type="button" class="btn btn-outline-secondary ml-2" @click="cancelForm">Cancelar</button>
                  </div>
               </div>
            </div>

         </div>
      </form>
   </div>
</template>

<script>
import countries from 'i18n-iso-countries'
import es from 'i18n-iso-countries/langs/es.json'
import { getPlayerByIdForEditing } from '@/api/connectionService'
import { normalizeIntoBackend, normalizeIntoForm } from '@/services/normalization_services'

export default {
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
               this.player.pro_since < 1800 || 
               this.player.pro_since > new Date().getFullYear() ) 
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
            this.player.height < 100 || 
            this.player.height > 270
         )
      },

      invalidWeight() {
         // allowed values 45-150
         return (
            this.player.weight < 45 || 
            this.player.weight > 150
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