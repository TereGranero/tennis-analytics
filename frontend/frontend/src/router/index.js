import { createRouter, createWebHistory } from 'vue-router'
import PlayersView from '@/views/PlayersView.vue'
import AddPlayerView from '@/views/AddPlayerView.vue'
import EditPlayerView from '@/views/EditPlayerView.vue'
import PlayerView from '@/views/PlayerView.vue'

const routes = [
  {
    path: "/players/:lastname?",  //optional param
    name: "Players",
    component: PlayersView,
    props: (route) => ({ lastname: route.params.lastname || null }),
  },

  {
    path: "/add-player",
    name: "AddPlayer",
    component: AddPlayerView,
  },

  {
    path: "/edit-player/:id",
    name: "EditPlayer",
    component: EditPlayerView,
    props: true,
  },

  {
    path: "/player/:id",
    name: "Player",
    component: PlayerView,
    props: true,
  },

];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router
