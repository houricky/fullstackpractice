"""
Tests for services.py — uses mongomock (no real Atlas connection needed).
"""

import mongomock
import pytest

import database
from models import CustomerCreate, CustomerUpdate
from services import (
    create_customer,
    delete_customer,
    get_all_customers,
    get_customer_by_id,
    get_next_account_id,
    get_next_customer_id,
    update_customer,
)


@pytest.fixture(autouse=True)
def mock_mongo():
    """Give each test a fresh in-memory MongoDB."""
    client = mongomock.MongoClient()
    db = client["bank_api"]
    database.customers_collection = db["customers"]
    database.accounts_collection = db["accounts"]
    yield


def _seed_test_data():
    database.customers_collection.insert_many(
        [
            {"id": 1, "name": "Alice Smith", "email": "alice@email.com"},
            {"id": 2, "name": "Bob Jones", "email": "bob@email.com"},
            {"id": 3, "name": "Charlie Brown", "email": "charlie@email.com"},
        ]
    )
    database.accounts_collection.insert_many(
        [
            {
                "id": 1,
                "customer_id": 1,
                "account_number": "A100",
                "account_type": "Checking",
                "balance": 5000,
            },
            {
                "id": 2,
                "customer_id": 1,
                "account_number": "A101",
                "account_type": "Savings",
                "balance": 8000,
            },
            {
                "id": 3,
                "customer_id": 2,
                "account_number": "A102",
                "account_type": "Checking",
                "balance": 2000,
            },
        ]
    )


def test_get_all_customers_success_links_accounts_to_customer():
    """Success: Alice (id=1) should get both of her accounts."""
    _seed_test_data()
    customers = get_all_customers()

    alice = customers[0]
    assert len(alice.accounts) == 2
    assert alice.accounts[0].account_number == "A100"
    assert alice.accounts[1].account_number == "A101"


def test_get_all_customers_failure_customer_with_no_accounts_stays_empty():
    """Failure case: Charlie (id=3) has no matching accounts."""
    _seed_test_data()
    customers = get_all_customers()

    charlie = customers[2]
    assert len(charlie.accounts) == 0


def test_get_next_customer_id_success_returns_one_after_max():
    """Success: with ids 1, 2, 3 seeded, next id should be 4."""
    _seed_test_data()
    assert get_next_customer_id() == 4


def test_get_next_customer_id_failure_empty_collection_starts_at_one():
    """Failure case: empty collection must return 1, not 4."""
    assert get_next_customer_id() == 1
    assert get_next_customer_id() != 4


def test_get_next_account_id_success_returns_one_after_max():
    """Success: with account ids 1, 2, 3 seeded, next id should be 4."""
    _seed_test_data()
    assert get_next_account_id() == 4


def test_get_next_account_id_failure_empty_collection_starts_at_one():
    """Failure case: empty collection must return 1, not 4."""
    assert get_next_account_id() == 1
    assert get_next_account_id() != 4


def test_create_customer_inserts_into_collection():
    _seed_test_data()
    created = create_customer(
        CustomerCreate(name="Diana", email="diana@email.com")
    )

    assert created.id == 4
    stored = database.customers_collection.find_one({"id": 4})
    assert stored is not None
    assert stored["name"] == "Diana"


def test_update_customer_success_changes_fields():
    _seed_test_data()
    updated = update_customer(
        1, CustomerUpdate(name="Alice Updated", email="alice.new@email.com")
    )

    assert updated is not None
    assert updated.name == "Alice Updated"
    assert updated.email == "alice.new@email.com"


def test_update_customer_failure_returns_none_when_missing():
    _seed_test_data()
    assert update_customer(999, CustomerUpdate(name="X", email="x@x.com")) is None


def test_delete_customer_success_removes_customer_and_accounts():
    _seed_test_data()
    assert delete_customer(1) is True
    assert get_customer_by_id(1) is None
    assert database.accounts_collection.count_documents({"customer_id": 1}) == 0


def test_delete_customer_failure_returns_false_when_missing():
    _seed_test_data()
    assert delete_customer(999) is False
