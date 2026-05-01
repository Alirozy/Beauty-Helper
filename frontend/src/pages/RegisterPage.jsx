import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/useAuth'

export function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({
    username: '',
    email: '',
    phone_number: '',
    password: '',
    password_confirm: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const onChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }))
  }

  const onSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      await register(form)
      navigate('/login')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="auth-box">
      <h2>Register</h2>
      <form onSubmit={onSubmit}>
        <input name="username" value={form.username} onChange={onChange} placeholder="Username" required />
        <input name="email" value={form.email} onChange={onChange} placeholder="Email" type="email" required />
        <input name="phone_number" value={form.phone_number} onChange={onChange} placeholder="Phone Number" />
        <input name="password" value={form.password} onChange={onChange} placeholder="Password" type="password" required />
        <input
          name="password_confirm"
          value={form.password_confirm}
          onChange={onChange}
          placeholder="Confirm Password"
          type="password"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      <p>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </section>
  )
}
