const BASE = process.env.VUE_APP_API_BASE || ''

export async function fetchHome() {
  const res = await fetch(`${BASE}/api/home`)
  if (!res.ok) throw new Error('Не удалось загрузить подборки')
  return res.json()
}
