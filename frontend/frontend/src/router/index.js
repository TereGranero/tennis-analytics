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
import Face2FaceSelectView from '@/views/Face2FaceSelectView.vue'
import Face2FaceShowView from '@/views/Face2FaceShowView.vue'
import ErrorView from '@/views/ErrorView.vue'

// Vue Router

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
      path: '/tournaments', // levels select, choose tournament
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
      path: '/face2face/select',
      name: 'Face2FaceSelect',
      component: Face2FaceSelectView,
   },

   {
      path: '/face2face/show/:player1Id/:player2Id',
      name: 'Face2FaceShow',
      component: Face2FaceShowView,
      props: true
   },

   {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: ErrorView,
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
