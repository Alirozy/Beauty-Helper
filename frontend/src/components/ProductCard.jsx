export function ProductCard({ product, actionButton }) {
  return (
    <article className="card">
      <img
        src={product.poster_url || 'https://placehold.co/360x220?text=No+Image'}
        alt={product.name}
        className="card-image"
      />
      <div className="card-content">
        <h3>{product.name}</h3>
        <p className="muted">
          {product.brand?.brand || 'Unknown brand'} - {product.type || 'Unknown type'}
        </p>
        <p>{product.description || 'No description available.'}</p>
        <p className="muted">Rating: {product.rating ?? 'N/A'}</p>
        {actionButton}
      </div>
    </article>
  )
}
