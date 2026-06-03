"""
Tests for services.py
"""

import database
from models import Account, Customer
from services import (
    get_next_account_id,
    get_next_customer_id,
    sync_customer_accounts,
)


def _reset_seed_data():
    """Put customers and accounts back to the default seed state."""
    database.accounts[:] = [
        Account(id=1, customer_id=1, account_number="A100", account_type="Checking", balance=5000),
        Account(id=2, customer_id=1, account_number="A101", account_type="Savings", balance=8000),
        Account(id=3, customer_id=2, account_number="A102", account_type="Checking", balance=2000),
    ]
    database.customers[:] = [
        Customer(id=1, name="Alice Smith", email="alice@email.com", accounts=[]),
        Customer(id=2, name="Bob Jones", email="bob@email.com", accounts=[]),
        Customer(id=3, name="Charlie Brown", email="charlie@email.com", accounts=[]),
    ]


# --- sync_customer_accounts ---


def test_sync_customer_accounts_success_links_accounts_to_customer():
    """Success: Alice (id=1) should get both of her accounts after sync."""
    _reset_seed_data()
    sync_customer_accounts()

    alice = database.customers[0]
    assert len(alice.accounts) == 2
    assert alice.accounts[0].account_number == "A100"
    assert alice.accounts[1].account_number == "A101"


def test_sync_customer_accounts_failure_customer_with_no_accounts_stays_empty():
    """Failure case: Charlie (id=3) has no rows in accounts — must stay empty."""
    _reset_seed_data()
    sync_customer_accounts()

    charlie = database.customers[2]
    assert len(charlie.accounts) == 0


# --- get_next_customer_id ---


def test_get_next_customer_id_success_returns_one_after_max():
    """Success: with ids 1, 2, 3 seeded, next id should be 4."""
    _reset_seed_data()
    assert get_next_customer_id() == 4


def test_get_next_customer_id_failure_empty_list_starts_at_one_not_four():
    """Failure case: empty database must return 1, not 4."""
    database.customers.clear()
    assert get_next_customer_id() == 1
    assert get_next_customer_id() != 4


# --- get_next_account_id ---


def test_get_next_account_id_success_returns_one_after_max():
    """Success: with account ids 1, 2, 3 seeded, next id should be 4."""
    _reset_seed_data()
    assert get_next_account_id() == 4


def test_get_next_account_id_failure_empty_list_starts_at_one_not_four():
    """Failure case: empty accounts must return 1, not 4."""
    database.accounts.clear()
    assert get_next_account_id() == 1
    assert get_next_account_id() != 4
