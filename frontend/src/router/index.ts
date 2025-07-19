import { createRouter, createWebHistory } from 'vue-router'
import Pronosticos from '../views/Pronosticos.vue'

const routes = [
  { path: '/', name: 'Pronosticos', component: Pronosticos }
]

const router = createRouter({
  history: createWebHistory('/pronosticos/'),
  routes
})

export default router

