const BASE = process.env.VUE_APP_API_BASE || ''

/**
 * Список товаров вишлиста
 * @returns {Promise<Array<{ id: string, name: string, imageUrl: string, link: string, price: string, createdAt: string }>>}
 */
export async function fetchWishlist() {
  const res = await fetch(`${BASE}/api/wishlist`)
  if (!res.ok) throw new Error('Не удалось загрузить вишлист')
  return res.json()
}

/**
 * Добавить товар
 * @param {{ name?: string, imageUrl?: string, link?: string, price?: string }} payload
 * @returns {Promise<{ id: string, name: string, imageUrl: string, link: string, price: string, createdAt: string }>}
 */
export async function createWishlistItem(payload) {
  const res = await fetch(`${BASE}/api/wishlist`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!res.ok) throw new Error('Не удалось добавить товар')
  return res.json()
}

/**
 * Удалить товар
 * @param {string} id
 */
export async function deleteWishlistItem(id) {
  const res = await fetch(`${BASE}/api/wishlist/${id}`, { method: 'DELETE' })
  if (!res.ok && res.status !== 204) throw new Error('Не удалось удалить товар')
}

