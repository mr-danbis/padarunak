const BASE = process.env.VUE_APP_API_BASE || ''

/**
 * Подборки для главной (категории с товарами)
 * @returns {Promise<{ collections: Array<{ id: number, name: string, products: Array<{ id: number, name: string, price: string, link: string, imageUrl: string }> }> }>}
 */
export async function fetchHome() {
  const res = await fetch(`${BASE}/api/home`)
  if (!res.ok) throw new Error('Не удалось загрузить подборки')
  return res.json()
}
