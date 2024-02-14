from decimal import Decimal
from bank import BankAccount, withdraw, deposit, AccountType
from stripe_service import StripePaymentService


def main() -> None:
    savings_account = BankAccount(AccountType.SAVINGS, "SA001", Decimal("1000"))
    checking_account = BankAccount(AccountType.CHECKING, "CA001", Decimal("500"))
    payment_service = StripePaymentService("sk_test_1234567890")
    # self.payment_service.set_api_key("sk_test_1234567890")

    # bank_service = BankService(payment_service)

    deposit(Decimal("200"), savings_account, payment_service)
    deposit(Decimal("300"), checking_account, payment_service)

    withdraw(Decimal("100"), savings_account, payment_service)
    withdraw(Decimal("200"), checking_account, payment_service)

    print(f"Savings Account Balance: {savings_account.balance}")
    print(f"Checking Account Balance: {checking_account.balance}")


if __name__ == "__main__":
    main()
