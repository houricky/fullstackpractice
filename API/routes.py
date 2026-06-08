from fastapi import APIRouter, HTTPException, status, Depends
from dependencies import get_current_user

from models import CustomerCreate, CustomerUpdate
from services import (
    create_customer,
    delete_customer,
    get_all_customers,
    get_customer_by_id,
    update_customer,
)

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


@router.put("/api/customers/{customer_id}")
def replace_customer(customer_id: int, customer_data: CustomerUpdate):
    customer = update_customer(customer_id, customer_data)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/api/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_customer(
    customer_id: int,
    _user: str = Depends(get_current_user),
):
    deleted = delete_customer(customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
