import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Pricing from '../views/Pricing.vue'
import Contact from '../views/Contact.vue'

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/about',
    component: About
  },
  {
    path: '/pricing',
    component: Pricing
  },
  {
    path: '/contact',
    component: Contact
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router