from dataclasses import dataclass
from decimal import Decimal

# from stripe_service import StripePaymentService
from typing import Protocol
from enum import Enum

# @dataclass
# class SavingsAccount:
#     account_number: str
#     balance: Decimal


# @dataclass
# class CheckingAccount:
#     account_number: str
#     balance: Decimal

class AccountType(Enum):
    SAVINGS = 'Savings'
    CHECKING = 'Checking'

@dataclass
class BankAccount:
    type: AccountType
    account_number: str
    balance: Decimal
    def deposit(self, amount: Decimal) -> None:
        print(
            f"Depositing {amount} into {self.type} Account {self.account_number}."
        )
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        print(
            f"Withdrawing {amount} from {self.type} Account {self.account_number}."
        )
        self.balance -= amount

class PaymentService(Protocol):
    def process_payment(self, amount: Decimal):
        ...

    def process_payout(self, amount: Decimal):
        ...


# class BankService:
#     def __init__(self, payment_service: PaymentService) -> None:
#         self.payment_service = payment_service

#     def deposit(self, amount: Decimal, account: BankAccount) -> None:
#         print(
#             f"Depositing {amount} into {account.type} Account {account.account_number}."
#         )
#         self.payment_service.process_payment(amount)
#         account.balance += amount

#     def withdraw(self, amount: Decimal, account: BankAccount) -> None:
#         print(
#             f"Withdrawing {amount} from {account.type} Account {account.account_number}."
#         )
#         self.payment_service.process_payout(amount)
#         account.balance -= amount

def deposit(amount: Decimal, account: BankAccount, payment_service: PaymentService):
    payment_service.process_payment(amount)
    account.deposit(amount)

def withdraw(amount: Decimal, account: BankAccount, payment_service: PaymentService):
    payment_service.process_payout(amount)
    account.withdraw(amount)
