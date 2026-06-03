from fastapi import APIRouter, HTTPException, status

from models import CustomerCreate
from services import create_customer, get_all_customers, get_customer_by_id

router = APIRouter()


@router.get("/api/customers")
def list_customers():
    return get_all_customers()


@router.get("/api/customers/{customer_id}")
def read_customer(customer_id: int):
    customer = get_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/api/customers", status_code=status.HTTP_201_CREATED)
def add_customer(customer_data: CustomerCreate):
    return create_customer(customer_data)
