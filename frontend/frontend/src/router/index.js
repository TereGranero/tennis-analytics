import { createRouter, createWebHistory } from 'vue-router'
import { authMiddleware } from '@/middleware/auth'
import HomeView from '@/views/HomeView.vue'
import PlayersView from '@/views/PlayersView.vue'
import AddPlayerView from '@/views/AddPlayerView.vue'
import EditPlayerView from '@/views/EditPlayerView.vue'
import PlayerView from '@/views/PlayerView.vue'
import RankingsView from '@/views/RankingsView.vue'
import TournamentsView from '@/views/TournamentsView.vue'
import TournamentWinnersView from '@/views/TournamentWinnersView.vue'
import LoginView from '@/views/LoginView.vue'

const routes = [
   {
      path: '/',
      name: 'Home',
      component: HomeView,
   },

   {
      path: '/login',
      name: 'Login',
      component: LoginView,
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
      meta: { requiresAuth: true }
   },

   {
      path: '/edit-player/:id',
      name: 'EditPlayer',
      component: EditPlayerView,
      props: true,
      meta: { requiresAuth: true }
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

   {
      path: "/404",
      redirect: "/error"
    }
];

const router = createRouter({
   history: createWebHistory(process.env.BASE_URL),
   routes,
});

router.beforeEach((to, from, next) => {
   if (to.meta.requiresAuth) {
      authMiddleware(to, from, next);
   } else {
      next();
   }
});

export default router
