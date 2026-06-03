import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.environ["MONGO_URI"])
db = client["bank_api"]

customers_collection = db["customers"]
accounts_collection = db["accounts"]

SEED_CUSTOMERS = [
    {"id": 1, "name": "Alice Smith", "email": "alice@email.com"},
    {"id": 2, "name": "Bob Jones", "email": "bob@email.com"},
    {"id": 3, "name": "Charlie Brown", "email": "charlie@email.com"},
]

SEED_ACCOUNTS = [
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


def seed_if_empty() -> None:
    """Insert starter data only when collections are empty."""
    if customers_collection.count_documents({}) == 0:
        customers_collection.insert_many(SEED_CUSTOMERS)

    if accounts_collection.count_documents({}) == 0:
        accounts_collection.insert_many(SEED_ACCOUNTS)
