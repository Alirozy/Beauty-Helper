import { useEffect, useMemo, useState } from 'react'
import { apiFetch, refreshAccessToken } from '../api/client'
import { AuthContext } from './auth-context'

function getInitialUser() {
  const raw = localStorage.getItem('user')
  if (!raw) return null
  try {
    return JSON.parse(raw)
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(getInitialUser())
  const [isAuthReady, setIsAuthReady] = useState(false)

  const login = async (credentials) => {
    const data = await apiFetch('/api/users/login/', {
      method: 'POST',
      body: JSON.stringify(credentials),
    })

    localStorage.setItem('accessToken', data.access)
    localStorage.setItem('refreshToken', data.refresh)
    localStorage.setItem('user', JSON.stringify(data.user))
    setUser(data.user)
  }

  const register = async (payload) => {
    await apiFetch('/api/users/register/', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  }

  const logout = async () => {
    try {
      const refresh = localStorage.getItem('refreshToken')
      if (refresh) {
        await apiFetch('/api/users/logout/', {
          method: 'POST',
          body: JSON.stringify({ refresh }),
        })
      }
    } catch {
      // Logout should clear local session even if API fails.
    }

    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
    setUser(null)
  }

  const updateUser = (nextUser) => {
    localStorage.setItem('user', JSON.stringify(nextUser))
    setUser(nextUser)
  }

  useEffect(() => {
    let mounted = true

    async function restoreSession() {
      const refresh = localStorage.getItem('refreshToken')

      if (!refresh) {
        if (mounted) setIsAuthReady(true)
        return
      }

      const access = localStorage.getItem('accessToken')
      if (!access) {
        const refreshed = await refreshAccessToken()
        if (!refreshed) {
          if (mounted) {
            localStorage.removeItem('user')
            setUser(null)
            setIsAuthReady(true)
          }
          return
        }
      }

      try {
        const me = await apiFetch('/api/users/me/')
        if (mounted) {
          const nextUser = { id: me.id, username: me.username, email: me.email }
          localStorage.setItem('user', JSON.stringify(nextUser))
          setUser(nextUser)
        }
      } catch {
        if (mounted) {
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          localStorage.removeItem('user')
          setUser(null)
        }
      } finally {
        if (mounted) setIsAuthReady(true)
      }
    }

    restoreSession()
    return () => {
      mounted = false
    }
  }, [])

  const value = useMemo(
    () => ({ user, login, register, logout, updateUser, isAuthReady }),
    [user, isAuthReady],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
