function CustomerDetail({ customer, onBack, onEdit }) {
  return (
    <section>
      <h2>Customer Details</h2>

      <dl>
        <dt>ID</dt>
        <dd>{customer.id}</dd>

        <dt>Name</dt>
        <dd>{customer.name}</dd>

        <dt>Email</dt>
        <dd>{customer.email}</dd>
      </dl>

      <h3>Accounts</h3>
      {customer.accounts.length === 0 ? (
        <p>No accounts.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Account #</th>
              <th>Type</th>
              <th>Balance</th>
            </tr>
          </thead>
          <tbody>
            {customer.accounts.map((account) => (
              <tr key={account.id}>
                <td>{account.account_number}</td>
                <td>{account.account_type}</td>
                <td>${account.balance.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div className="actions">
        <button type="button" onClick={onBack}>
          Back
        </button>
        <button type="button" onClick={onEdit}>
          Edit
        </button>
      </div>
    </section>
  )
}

export default CustomerDetail
