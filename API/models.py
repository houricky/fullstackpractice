from pydantic import BaseModel
from typing import List


class Account(BaseModel):
    id: int
    customer_id: int
    account_number: str
    account_type: str
    balance: float


class Customer(BaseModel):
    id: int
    name: str
    email: str
    accounts: List[Account] = []


class CustomerCreate(BaseModel):
    name: str
    email: str


class CustomerUpdate(BaseModel):
    """Body for PUT — client sends the full updated customer fields."""
    name: str
    email: str


class AccountCreate(BaseModel):
    customer_id: int
    account_number: str
    account_type: str
    balance: float

class User(BaseModel):
    id: int
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"