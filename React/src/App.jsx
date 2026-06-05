import { useState } from 'react'
import CustomerList from './components/CustomerList'
import CustomerForm from './components/CustomerForm'
import CustomerDetail from './components/CustomerDetail'
import './App.css'

// placeholder data — replace with API calls later
const MOCK_CUSTOMERS = [
  {
    id: 1,
    name: 'Alice Smith',
    email: 'alice@email.com',
    accounts: [
      { id: 1, account_number: 'A100', account_type: 'Checking', balance: 5000 },
      { id: 2, account_number: 'A101', account_type: 'Savings', balance: 8000 },
    ],
  },
  {
    id: 2,
    name: 'Bob Jones',
    email: 'bob@email.com',
    accounts: [
      { id: 3, account_number: 'A102', account_type: 'Checking', balance: 2000 },
    ],
  },
  {
    id: 3,
    name: 'Charlie Brown',
    email: 'charlie@email.com',
    accounts: [],
  },
]

function App() {
  const [view, setView] = useState('list')
  const [selectedId, setSelectedId] = useState(null)

  const selectedCustomer = MOCK_CUSTOMERS.find((c) => c.id === selectedId)

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

  function handleDelete(id) {
    // TODO: call DELETE /api/customers/{id}
    console.log('delete customer', id)
  }

  function handleSave(customer) {
    if (view === 'create') {
      // TODO: call POST /api/customers
      console.log('create customer', customer)
    } else {
      // TODO: call PUT /api/customers/{id}
      console.log('update customer', customer)
    }
    goToList()
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

      <main>
        {view === 'list' && (
          <CustomerList
            customers={MOCK_CUSTOMERS}
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
