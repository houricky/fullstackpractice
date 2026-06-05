function CustomerList({ customers, onView, onEdit, onDelete }) {
  return (
    <section>
      <h2>Customers</h2>

      {customers.length === 0 ? (
        <p>No customers yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Accounts</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((customer) => (
              <tr key={customer.id}>
                <td>{customer.id}</td>
                <td>{customer.name}</td>
                <td>{customer.email}</td>
                <td>{customer.accounts.length}</td>
                <td className="actions">
                  <button type="button" onClick={() => onView(customer.id)}>
                    View
                  </button>
                  <button type="button" onClick={() => onEdit(customer.id)}>
                    Edit
                  </button>
                  <button type="button" onClick={() => onDelete(customer.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  )
}

export default CustomerList
