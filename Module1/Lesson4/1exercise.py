"""Custom Exception: Create a custom exception called 
InsufficientFundsError that is raised when a user tries 
to withdraw more money than they have in their account. 
Include the account balance in the exception message."""

import decimal

class CustomError(Exception):
    pass

class InsufficientFundsError(CustomError):
    def __init__(self, balance):
        message = f"Insufficient funds: current balance is {balance}"
        super().__init__(message)
        self.balance = balance

class Account():
    def __init__(self, user: str, balance: decimal.Decimal):
        self.user = user
        self.balance = balance

    def deposit(self, amount: decimal.Decimal):
        print("Depositing: ", amount)
        self.balance += amount
        print("Balance: ", self.balance)

    def withdraw(self, amount: decimal.Decimal):
        print("Withdrawing: ", amount)
        if self.balance - amount < 0:
            raise InsufficientFundsError(self.balance)
        self.balance -= amount
        print("Balance: ", self.balance)

if __name__ == "__main__":
    acc = Account("Bob", 0)
    try:
        acc.deposit(100)
        acc.withdraw(50)
        acc.withdraw(70)
    except InsufficientFundsError as e:
        print(e)