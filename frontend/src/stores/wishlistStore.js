import { defineStore } from 'pinia'
import { fetchWishlist, createWishlistItem, deleteWishlistItem } from '../api/wishlist'

export const useWishlistStore = defineStore('wishlist', {
  state: () => ({
    items: [],
    loading: false,
    error: null
  }),

  getters: {
    wishlistCount: (state) => state.items.length
  },

  actions: {
    async fetchWishlist() {
      this.loading = true
      this.error = null
      try {
        this.items = await fetchWishlist()
      } catch (e) {
        this.error = e.message || 'Ошибка загрузки'
        this.items = []
      } finally {
        this.loading = false
      }
    },

    async addItem(payload) {
      const item = await createWishlistItem(payload)
      this.items = [item, ...this.items]
      return item.id
    },

    async removeItem(id) {
      await deleteWishlistItem(id)
      this.items = this.items.filter((i) => i.id !== id)
    }
  }
})
