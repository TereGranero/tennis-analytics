import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import PlayersView from '@/views/PlayersView.vue'
import AddPlayerView from '@/views/AddPlayerView.vue'
import EditPlayerView from '@/views/EditPlayerView.vue'
import PlayerView from '@/views/PlayerView.vue'
import RankingsView from '@/views/RankingsView.vue'
import TournamentsView from '@/views/TournamentsView.vue'
import TournamentWinnersView from '@/views/TournamentWinnersView.vue'

const routes = [
   {
      path: '/',
      name: 'Home',
      component: HomeView,
   },

   {
      path: '/players/:lastname?',  //optional param
      name: 'Players',
      component: PlayersView,
      props: (route) => ({ lastname: route.params.lastname || null }),
   },

   {
      path: '/add-player',
      name: 'AddPlayer',
      component: AddPlayerView,
   },

   {
      path: '/edit-player/:id',
      name: 'EditPlayer',
      component: EditPlayerView,
      props: true,
   },

   {
      path: '/player/:id',
      name: 'Player',
      component: PlayerView,
      props: true,
   },

   {
      path: '/rankings',
      name: 'Rankings',
      component: RankingsView,
   },

   {
      path: '/tournaments', // levels select, chose tournament
      name: 'Tournaments',
      component: TournamentsView,
   },

   {
      path: '/tournaments/winners/:tournamentSlug',
      name: 'TournamentWinners',
      component: TournamentWinnersView,
      props: true
   },
];

const router = createRouter({
   history: createWebHistory(process.env.BASE_URL),
   routes,
});

export default router
