import { defineStore } from 'pinia'
import { fetchMe, loginUrl, logoutUrl } from '../api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    loading: true
  }),

  getters: {
    isLoggedIn: (state) => !!state.user
  },

  actions: {
    async fetchUser() {
      this.loading = true
      try {
        this.user = await fetchMe()
      } catch {
        this.user = null
      } finally {
        this.loading = false
      }
    },

    login() {
      window.location.href = loginUrl()
    },

    logout() {
      window.location.href = logoutUrl()
    }
  }
})
