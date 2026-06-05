import { useEffect, useState } from 'react'
import * as customerApi from './api/customers'
import CustomerList from './components/CustomerList'
import CustomerForm from './components/CustomerForm'
import CustomerDetail from './components/CustomerDetail'
import './App.css'

function App() {
  const [view, setView] = useState('list')
  const [selectedId, setSelectedId] = useState(null)
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const selectedCustomer = customers.find((c) => c.id === selectedId)

  async function loadCustomers() {
    setLoading(true)
    setError(null)
    try {
      const data = await customerApi.getCustomers()
      setCustomers(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadCustomers()
  }, [])

  function goToList() {
    setView('list')
    setSelectedId(null)
  }

  function handleView(id) {
    setSelectedId(id)
    setView('detail')
  }

  function handleCreate() {
    setSelectedId(null)
    setView('create')
  }

  function handleEdit(id) {
    setSelectedId(id)
    setView('edit')
  }

  async function handleDelete(id) {
    setError(null)
    try {
      await customerApi.deleteCustomer(id)
      await loadCustomers()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleSave(customer) {
    setError(null)
    try {
      if (view === 'create') {
        await customerApi.createCustomer({
          name: customer.name,
          email: customer.email,
        })
      } else {
        await customerApi.updateCustomer(customer.id, {
          name: customer.name,
          email: customer.email,
        })
      }
      await loadCustomers()
      goToList()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>Bank App</h1>
        <nav>
          <button type="button" onClick={goToList}>
            Customers
          </button>
          <button type="button" onClick={handleCreate}>
            New Customer
          </button>
        </nav>
      </header>

      {error && <p className="error">{error}</p>}

      <main>
        {loading && view === 'list' && <p>Loading...</p>}

        {!loading && view === 'list' && (
          <CustomerList
            customers={customers}
            onView={handleView}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        )}

        {view === 'detail' && selectedCustomer && (
          <CustomerDetail
            customer={selectedCustomer}
            onBack={goToList}
            onEdit={() => handleEdit(selectedCustomer.id)}
          />
        )}

        {view === 'create' && (
          <CustomerForm
            title="New Customer"
            onSave={handleSave}
            onCancel={goToList}
          />
        )}

        {view === 'edit' && selectedCustomer && (
          <CustomerForm
            title="Edit Customer"
            customer={selectedCustomer}
            onSave={handleSave}
            onCancel={goToList}
          />
        )}
      </main>
    </div>
  )
}

export default App
