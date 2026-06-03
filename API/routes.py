from fastapi import APIRouter, HTTPException, status
from database import customers
from models import Customer, CustomerCreate
from services import sync_customer_accounts, get_next_customer_id

router = APIRouter()


@router.get("/api/customers")
def get_all_customers():
    sync_customer_accounts()
    return customers


@router.get("/api/customers/{customer_id}")
def get_customer_by_id(customer_id: int):
    sync_customer_accounts()

    for customer in customers:
        if customer.id == customer_id:
            return customer

    raise HTTPException(status_code=404, detail="Customer not found")


@router.post("/api/customers", status_code=status.HTTP_201_CREATED)
def create_customer(customer_data: CustomerCreate):
    new_customer = Customer(
        id=get_next_customer_id(),
        name=customer_data.name,
        email=customer_data.email,
        accounts=[]
    )

    customers.append(new_customer)

    return new_customer
