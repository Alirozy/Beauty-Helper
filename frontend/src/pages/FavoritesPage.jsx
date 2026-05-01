import { useEffect, useState } from 'react'
import { apiFetch } from '../api/client'
import { ProductCard } from '../components/ProductCard'

export function FavoritesPage() {
  const [favorites, setFavorites] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let mounted = true

    async function loadInitialFavorites() {
      try {
        const data = await apiFetch('/api/users/favorites/')
        if (mounted) {
          setFavorites(data.results || [])
        }
      } catch (err) {
        if (mounted) {
          setError(err.message)
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    loadInitialFavorites()
    return () => {
      mounted = false
    }
  }, [])

  const removeFavorite = async (favoriteId) => {
    try {
      await apiFetch(`/api/users/favorites/${favoriteId}/`, { method: 'DELETE' })
      setFavorites((prev) => prev.filter((item) => item.id !== favoriteId))
    } catch (err) {
      alert(err.message)
    }
  }

  return (
    <section>
      <h2>My Favorites</h2>
      {error && <p className="error">{error}</p>}
      {loading && <p>Loading favorites...</p>}
      {!loading && !favorites.length && <p>No favorites yet.</p>}

      <div className="grid">
        {favorites.map((favorite) => (
          <ProductCard
            key={favorite.id}
            product={favorite.product_details}
            actionButton={
              <button type="button" onClick={() => removeFavorite(favorite.id)}>
                Remove
              </button>
            }
          />
        ))}
      </div>
    </section>
  )
}
