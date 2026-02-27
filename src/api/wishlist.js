const BASE = process.env.VUE_APP_API_BASE || ''

export async function fetchWishlist() {
  const res = await fetch(`${BASE}/api/wishlist`)
  if (!res.ok) throw new Error('Не удалось загрузить вишлист')
  return res.json()
}

export async function createWishlistItem(payload) {
  const res = await fetch(`${BASE}/api/wishlist`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!res.ok) throw new Error('Не удалось добавить товар')
  return res.json()
}

export async function deleteWishlistItem(id) {
  const res = await fetch(`${BASE}/api/wishlist/${id}`, { method: 'DELETE' })
  if (!res.ok && res.status !== 204) throw new Error('Не удалось удалить товар')
}

export async function fetchLinkPreview(url) {
  const encoded = encodeURIComponent(url)
  const res = await fetch(`${BASE}/api/link-preview?url=${encoded}`)
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.error || 'Не удалось загрузить данные по ссылке')
  return data
}

