import { useEffect, useState } from 'react'
import { apiFetch } from '../api/client'
import { useAuth } from '../context/useAuth'

const INITIAL_FORM = {
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  phone_number: '',
  birth_date: '',
  skin_type: '',
  allergies: '',
  preferred_brands: '',
  preferred_product_types: '',
}

export function ProfilePage() {
  const { user, updateUser } = useAuth()
  const [form, setForm] = useState(INITIAL_FORM)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    let mounted = true

    async function loadProfile() {
      try {
        const data = await apiFetch('/api/users/me/')
        if (!mounted) return
        setForm({
          username: data.username || '',
          email: data.email || '',
          first_name: data.first_name || '',
          last_name: data.last_name || '',
          phone_number: data.phone_number || '',
          birth_date: data.birth_date || '',
          skin_type: data.skin_type || '',
          allergies: data.allergies || '',
          preferred_brands: data.preferred_brands || '',
          preferred_product_types: data.preferred_product_types || '',
        })
      } catch (err) {
        if (mounted) setError(err.message)
      } finally {
        if (mounted) setLoading(false)
      }
    }

    loadProfile()
    return () => {
      mounted = false
    }
  }, [])

  const onChange = (event) => {
    setSuccess('')
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const onSubmit = async (event) => {
    event.preventDefault()
    setSaving(true)
    setError('')
    setSuccess('')

    try {
      const payload = {
        ...form,
        birth_date: form.birth_date || null,
        phone_number: form.phone_number || null,
      }
      const data = await apiFetch('/api/users/me/', {
        method: 'PATCH',
        body: JSON.stringify(payload),
      })

      updateUser({
        id: user?.id,
        username: data.username,
        email: data.email,
      })
      setSuccess('Profile updated successfully.')
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return <p>Loading profile...</p>
  }

  return (
    <section className="profile-box">
      <h2>Edit Profile</h2>
      <form onSubmit={onSubmit} className="profile-form">
        <input name="username" value={form.username} onChange={onChange} placeholder="Username" required />
        <input name="email" type="email" value={form.email} onChange={onChange} placeholder="Email" required />
        <input name="first_name" value={form.first_name} onChange={onChange} placeholder="First Name" />
        <input name="last_name" value={form.last_name} onChange={onChange} placeholder="Last Name" />
        <input name="phone_number" value={form.phone_number} onChange={onChange} placeholder="Phone Number" />
        <input name="birth_date" type="date" value={form.birth_date} onChange={onChange} />
        <input name="skin_type" value={form.skin_type} onChange={onChange} placeholder="Skin Type" />
        <textarea name="allergies" value={form.allergies} onChange={onChange} placeholder="Allergies" />
        <textarea
          name="preferred_brands"
          value={form.preferred_brands}
          onChange={onChange}
          placeholder="Preferred Brands"
        />
        <textarea
          name="preferred_product_types"
          value={form.preferred_product_types}
          onChange={onChange}
          placeholder="Preferred Product Types"
        />

        <button type="submit" disabled={saving}>
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}
      {success && <p className="success">{success}</p>}
    </section>
  )
}
