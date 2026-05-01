import { useEffect, useState } from 'react'
import { apiFetch } from '../api/client'
import { ProductCard } from '../components/ProductCard'

export function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [limit, setLimit] = useState(10)

  useEffect(() => {
    let mounted = true

    async function loadInitialRecommendations() {
      try {
        const data = await apiFetch('/api/recommendations/')
        if (mounted) {
          setRecommendations(data.results || [])
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

    loadInitialRecommendations()
    return () => {
      mounted = false
    }
  }, [])

  const generateRecommendations = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await apiFetch('/api/recommendations/generate/', {
        method: 'POST',
        body: JSON.stringify({ limit }),
      })
      setRecommendations(data.results || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <h2>Recommendations</h2>
      <div className="toolbar">
        <input
          type="number"
          min="1"
          max="50"
          value={limit}
          onChange={(e) => setLimit(Number(e.target.value))}
        />
        <button type="button" onClick={generateRecommendations} disabled={loading}>
          Generate
        </button>
      </div>

      {error && <p className="error">{error}</p>}
      {loading && <p>Processing...</p>}
      {!loading && !recommendations.length && <p>No recommendations yet.</p>}

      <div className="grid">
        {recommendations.map((item) => (
          <ProductCard
            key={item.id}
            product={item.product_details}
            actionButton={<p className="muted">Reason: {item.reason || 'No reason provided.'}</p>}
          />
        ))}
      </div>
    </section>
  )
}
