from models import Customer, Account


accounts = [
    Account(id=1, customer_id=1, account_number="A100", account_type="Checking", balance=5000),
    Account(id=2, customer_id=1, account_number="A101", account_type="Savings", balance=8000),
    Account(id=3, customer_id=2, account_number="A102", account_type="Checking", balance=2000),
]


customers = [
    Customer(id=1, name="Alice Smith", email="alice@email.com", accounts=[]),
    Customer(id=2, name="Bob Jones", email="bob@email.com", accounts=[]),
    Customer(id=3, name="Charlie Brown", email="charlie@email.com", accounts=[]),
]
