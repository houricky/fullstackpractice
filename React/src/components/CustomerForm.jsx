import { useState } from 'react'

function CustomerForm({ title, customer, onSave, onCancel }) {
  const [name, setName] = useState(customer?.name ?? '')
  const [email, setEmail] = useState(customer?.email ?? '')

  function handleSubmit(e) {
    e.preventDefault()
    onSave({
      id: customer?.id,
      name,
      email,
    })
  }

  return (
    <section>
      <h2>{title}</h2>

      <form onSubmit={handleSubmit}>
        <label>
          Name
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </label>

        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>

        <div className="actions">
          <button type="submit">Save</button>
          <button type="button" onClick={onCancel}>
            Cancel
          </button>
        </div>
      </form>
    </section>
  )
}

export default CustomerForm
