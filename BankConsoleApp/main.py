"""
Banking application in Python.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional


class ITransaction(ABC):
    def print_receipt(self):
        pass


class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


class Admin(User):
    def __init__(self) -> None:
        super().__init__("admin", "admin123")

class Customer(User):
    def __init__(
        self,
        customer_id: int,
        name: str,
        accounts: List[Account],
        username: str,
        password: str,
    ) -> None:
        super().__init__(username, password)
        self._customer_id = customer_id
        self._name = name
        self._accounts = accounts

    @property
    def customer_id(self) -> int:
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value: int) -> None:
        self._customer_id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def accounts(self) -> List[Account]:
        return self._accounts

    @accounts.setter
    def accounts(self, value: List[Account]) -> None:
        self._accounts = value

    def __str__(self) -> str:
        return (
            f"Customer{{id={self._customer_id}, "
            f"name='{self._name}', accounts={self._accounts}}}"
        )


class Account(ITransaction, ABC):
    def __init__(
        self,
        account_number: str,
        account_holder: Customer,
        balance: Decimal,
    ) -> None:
        self._account_number = account_number
        self._account_holder = account_holder
        self._balance = balance

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def account_holder(self) -> Customer:
        return self._account_holder

    @property
    def balance(self) -> Decimal:
        return self._balance

    @balance.setter
    def balance(self, value: Decimal) -> None:
        self._balance = value

    def deposit(self, amount: Decimal) -> None:
        """Virtual in C# / overridable in Java — base deposit logic."""
        if amount > 0:
            self._balance += amount

    def withdraw(self, amount: Decimal) -> bool:
        """Each account type defines its own withdrawal rules."""
        ...

    def add_interest(self) -> Decimal:
        """Java had this on Account; savings 3%, checking 2%."""
        ...

    def print_receipt(self) -> None:
        print(
            f"Receipt — Account {self._account_number} "
            f"({self.__class__.__name__}): balance ${self._balance:.2f}"
        )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}{{number={self._account_number}, balance={self._balance}}}"


class SavingsAccount(Account):
    account_type = "SavingsAccount"

    def __init__(
        self,
        account_number: str,
        account_holder: Customer,
        balance: Decimal,
        interest_rate: Decimal = Decimal("0.03"),
    ) -> None:
        super().__init__(account_number, account_holder, balance)
        self._interest_rate = interest_rate

    @property
    def interest_rate(self) -> Decimal:
        return self._interest_rate

    def withdraw(self, amount: Decimal) -> bool:
        if amount <= 0:
            return False
        if self._balance - amount < Decimal("100"):
            print("Savings withdrawal denied: balance would fall below $100.")
            return False
        self._balance -= amount
        return True

    def add_interest(self) -> Decimal:
        self._balance += self._balance * self._interest_rate
        return self._balance


class CheckingAccount(Account):
    account_type = "CheckingAccount"

    def __init__(
        self,
        account_number: str,
        account_holder: Customer,
        balance: Decimal,
        overdraft_limit: Decimal = Decimal("500"),
    ) -> None:
        super().__init__(account_number, account_holder, balance)
        self._overdraft_limit = overdraft_limit

    @property
    def overdraft_limit(self) -> Decimal:
        return self._overdraft_limit

    def withdraw(self, amount: Decimal) -> bool:
        if amount <= 0:
            return False
        if self._balance - amount < -self._overdraft_limit:
            print(
                f"Checking withdrawal denied: exceeds overdraft limit "
                f"(${self._overdraft_limit})."
            )
            return False
        self._balance -= amount
        return True

    def add_interest(self) -> Decimal:
        rate = Decimal("0.02")
        self._balance += self._balance * rate
        return self._balance


def welcome() -> None:
    print("Welcome to ABC Digital Bank")


def login(users: List[User]) -> str:
    """
    Returns 'admin', a customer username, or 'validation_failed'.
    Java: Scanner.nextLine() with space-separated username password.
    """
    print("Please enter username and password, space separated")
    entered = input().strip()
    parts = entered.split()
    if len(parts) != 2:
        return "validation_failed"

    username, password = parts[0], parts[1]

    if username == "admin" and password == "admin123":
        return "admin"

    for user in users:
        if user.username == username and user.password == password:
            return user.username

    return "validation_failed"


def seed_database(customers: List[Customer], users: List[User]) -> None:
    """
    Step 6: Populate the in-memory customer database with default test data
    so logins, lookups, and withdrawals work immediately on startup.
    """
    u1 = User("richard", "richard123")
    u2 = User("rohit", "rohit123")
    users.extend([u1, u2])

    c1 = Customer(1, "richard", [], u1.username, u1.password)
    c2 = Customer(2, "rohit", [], u2.username, u2.password)
    customers.extend([c1, c2])

    c1.accounts.extend(
        [
            SavingsAccount("SAV-001", c1, Decimal("1500"), Decimal("0.03")),
            CheckingAccount("CHK-001", c1, Decimal("350"), Decimal("500")),
        ]
    )
    c2.accounts.append(
        SavingsAccount("SAV-002", c2, Decimal("800"), Decimal("0.03"))
    )

    print(
        f"Seeded {len(customers)} customers with "
        f"{sum(len(c.accounts) for c in customers)} accounts."
    )


def customer_dashboard(
    username: str, customers: List[Customer]
) -> None:
    customer = next((c for c in customers if c.username == username), None)
    if customer is None:
        print("Customer record not found.")
        return

    print(f"Welcome customer, {username}")
    while True:
        print("\n1. See my accounts")
        print("2. Read account balance")
        print("3. Print receipt (ITransaction)")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            if not customer.accounts:
                print("No accounts linked.")
            for acc in customer.accounts:
                print(f"  {acc}")
        elif choice == "2":
            if not customer.accounts:
                print("No accounts linked.")
            for acc in customer.accounts:
                print(f"  {acc.account_number}: ${acc.balance:.2f}")
        elif choice == "3":
            for acc in customer.accounts:
                acc.print_receipt()
        elif choice == "4":
            break
        else:
            print("Invalid option.")


def admin_dashboard(customers: List[Customer]) -> None:
    print("Welcome Admin")
    while True:
        print("\n1. See all customers")
        print("2. See all accounts")
        print("3. Delete an account")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            for c in customers:
                print(c)
        elif choice == "2":
            for c in customers:
                for acc in c.accounts:
                    print(f"  {c.name}: {acc}")
        elif choice == "3":
            acct_num = input("Account number to delete: ").strip()
            deleted = False
            for c in customers:
                for acc in list(c.accounts):
                    if acc.account_number == acct_num:
                        c.accounts.remove(acc)
                        print(f"Deleted {acct_num}")
                        deleted = True
                        break
                if deleted:
                    break
            if not deleted:
                print("Account not found.")
        elif choice == "4":
            break
        else:
            print("Invalid option.")


def main() -> None:
    # Step 6: dynamic in-memory customer database (created when the app starts)
    customers: List[Customer] = []
    users: List[User] = []
    seed_database(customers, users)

    # Core application loop — return to welcome after each session
    while True:
        welcome()
        login_result = login(users)

        if login_result == "validation_failed":
            print("Validation Failed")
            retry = input("Try again? (y/n): ").strip().lower()
            if retry != "y":
                print("Goodbye.")
                break
            continue

        if login_result == "admin":
            admin_dashboard(customers)
        else:
            customer_dashboard(login_result, customers)
        break


if __name__ == "__main__":
    main()
