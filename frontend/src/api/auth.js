const BASE = process.env.VUE_APP_API_BASE || ''

export function loginUrl() {
  return `${BASE}/api/auth/login`
}

export function logoutUrl() {
  return `${BASE}/api/auth/logout`
}

export async function fetchMe() {
  const res = await fetch(`${BASE}/api/auth/me`, { credentials: 'include' })
  if (res.status === 401) return null
  if (!res.ok) throw new Error('Ошибка проверки входа')
  return res.json()
}
