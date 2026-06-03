import database
from models import Account, Customer, CustomerCreate


def _doc_to_account(doc: dict) -> Account:
    data = dict(doc)
    data.pop("_id", None)
    return Account(**data)


def _doc_to_customer(doc: dict, with_accounts: bool = False) -> Customer:
    data = dict(doc)
    data.pop("_id", None)
    customer = Customer(**data)

    if with_accounts:
        account_docs = database.accounts_collection.find(
            {"customer_id": customer.id}
        )
        customer.accounts = [_doc_to_account(doc) for doc in account_docs]

    return customer


def get_all_customers() -> list[Customer]:
    customers = []
    for doc in database.customers_collection.find().sort("id", 1):
        customers.append(_doc_to_customer(doc, with_accounts=True))
    return customers


def get_customer_by_id(customer_id: int) -> Customer | None:
    doc = database.customers_collection.find_one({"id": customer_id})
    if doc is None:
        return None
    return _doc_to_customer(doc, with_accounts=True)


def create_customer(customer_data: CustomerCreate) -> Customer:
    new_id = get_next_customer_id()
    doc = {
        "id": new_id,
        "name": customer_data.name,
        "email": customer_data.email,
    }
    database.customers_collection.insert_one(doc)
    return Customer(id=new_id, name=customer_data.name, email=customer_data.email)


def get_next_customer_id() -> int:
    latest = database.customers_collection.find_one(sort=[("id", -1)])
    if latest is None:
        return 1
    return latest["id"] + 1


def get_next_account_id() -> int:
    latest = database.accounts_collection.find_one(sort=[("id", -1)])
    if latest is None:
        return 1
    return latest["id"] + 1
