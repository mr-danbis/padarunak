import { storeToRefs } from 'pinia'
import { useWishlistStore } from '../stores/wishlistStore'

/**
 * Хук вишлиста — читает и изменяет глобальный стор вишлиста.
 */
export function useWishlist() {
  const store = useWishlistStore()
  const { items, loading, error } = storeToRefs(store)
  return {
    items,
    loading,
    error,
    fetchWishlist: () => store.fetchWishlist(),
    addItem: (payload) => store.addItem(payload),
    removeItem: (id) => store.removeItem(id)
  }
}
