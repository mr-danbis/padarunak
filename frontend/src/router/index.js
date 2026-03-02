import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home/Home.vue'
import Account from '../views/Account/Account.vue'

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/wishlist',
    redirect: { path: '/account', query: { section: 'wishlist' } }
  },
  {
    path: '/account',
    component: Account
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
