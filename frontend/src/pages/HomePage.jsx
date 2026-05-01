import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiFetch } from '../api/client'
import { ProductCard } from '../components/ProductCard'
import { useAuth } from '../context/useAuth'

const BACKEND_PAGE_SIZE = 20

export function HomePage() {
  const { user } = useAuth()
  const [products, setProducts] = useState([])
  const [search, setSearch] = useState('')
  const [activeSearch, setActiveSearch] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [pageSize] = useState(BACKEND_PAGE_SIZE)
  const [totalCount, setTotalCount] = useState(0)
  const [hasNext, setHasNext] = useState(false)
  const [hasPrevious, setHasPrevious] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const totalPages = Math.max(1, Math.ceil(totalCount / pageSize))

  const loadProducts = async (searchValue = '', page = 1) => {
    setLoading(true)
    setError('')
    try {
      const params = new URLSearchParams()
      params.set('page', String(page))
      if (searchValue) {
        params.set('search', searchValue)
      }
      const data = await apiFetch(`/api/products/list/?${params.toString()}`)
      setProducts(data.results || [])
      setTotalCount(data.count || 0)
      setHasNext(Boolean(data.next))
      setHasPrevious(Boolean(data.previous))
      setCurrentPage(page)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    let mounted = true

    async function loadInitialProducts() {
      try {
        const data = await apiFetch('/api/products/list/?page=1')
        if (mounted) {
          setProducts(data.results || [])
          setTotalCount(data.count || 0)
          setHasNext(Boolean(data.next))
          setHasPrevious(Boolean(data.previous))
          setCurrentPage(1)
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

    loadInitialProducts()
    return () => {
      mounted = false
    }
  }, [])

  const onSearch = (event) => {
    event.preventDefault()
    const nextSearch = search.trim()
    setActiveSearch(nextSearch)
    loadProducts(nextSearch, 1)
  }

  const goToNextPage = () => {
    if (hasNext && !loading) {
      loadProducts(activeSearch, currentPage + 1)
    }
  }

  const goToPreviousPage = () => {
    if (hasPrevious && !loading) {
      loadProducts(activeSearch, currentPage - 1)
    }
  }

  const addToFavorites = async (productId) => {
    try {
      await apiFetch('/api/users/favorites/', {
        method: 'POST',
        body: JSON.stringify({ product: productId }),
      })
      alert('Product added to favorites.')
    } catch (err) {
      alert(err.message)
    }
  }

  return (
    <section>
      <form onSubmit={onSearch} className="toolbar">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by product name or description"
        />
        <button type="submit">Search</button>
      </form>

      {error && <p className="error">{error}</p>}
      {loading && <p>Loading products...</p>}

      {!loading && !products.length && <p>No products found.</p>}

      <div className="grid">
        {products.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            actionButton={
              user ? (
                <button type="button" onClick={() => addToFavorites(product.id)}>
                  Add Favorite
                </button>
              ) : (
                <Link to="/login">Login to favorite</Link>
              )
            }
          />
        ))}
      </div>

      {!loading && totalCount > 0 && (
        <div className="pagination">
          <button type="button" onClick={goToPreviousPage} disabled={!hasPrevious}>
            Previous
          </button>
          <span>
            Page {currentPage} / {totalPages} - Total {totalCount} products
          </span>
          <button type="button" onClick={goToNextPage} disabled={!hasNext}>
            Next
          </button>
        </div>
      )}
    </section>
  )
}
