from database import customers, accounts


def sync_customer_accounts():
    for customer in customers:
        customer.accounts = []

        for account in accounts:
            if account.customer_id == customer.id:
                customer.accounts.append(account)


def get_next_customer_id():
    if len(customers) == 0:
        return 1

    return max(customer.id for customer in customers) + 1


def get_next_account_id():
    if len(accounts) == 0:
        return 1

    return max(account.id for account in accounts) + 1
