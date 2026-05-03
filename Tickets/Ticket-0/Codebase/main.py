"""
Main banking application demo.
Shows account creation, deposits, withdrawals, interest calculations, and transfers.
"""

from bank import Bank
from interest import InterestCalculator
from transactions import TransactionManager


def demo_banking_system():
    """Demonstrate a complete banking system workflow."""

    # Create a bank
    bank = Bank("SimpleBank")
    print(f"=== Welcome to {bank.bank_name} ===\n")

    # Create accounts
    print("Creating accounts...")
    checking = bank.create_account("ACC001", "1234", "Alice Johnson", 1000.0)
    savings = bank.create_account("ACC002", "5678", "Bob Smith", 500.0)
    print(f"✓ Created checking account for {checking.holder_name} with balance: ${checking.balance:.2f}")
    print(f"✓ Created savings account for {savings.holder_name} with balance: ${savings.balance:.2f}\n")

    # Deposits
    print("=== Deposits ===")
    checking.deposit(250.0, "Paycheck")
    print(f"Alice deposits $250 → New balance: ${checking.balance:.2f}")
    savings.deposit(100.0, "Bonus")
    print(f"Bob deposits $100 → New balance: ${savings.balance:.2f}\n")

    # Withdrawals
    print("=== Withdrawals ===")
    checking.withdraw(150.0, "ATM Withdrawal")
    print(f"Alice withdraws $150 → New balance: ${checking.balance:.2f}")
    savings.withdraw(50.0, "Cash Withdrawal")
    print(f"Bob withdraws $50 → New balance: ${savings.balance:.2f}\n")

    # Interest calculation
    print("=== Interest Calculation ===")
    annual_rate = 0.03  # 3% APY
    simple_interest = InterestCalculator.simple_interest(savings.balance, annual_rate, 1)
    print(f"Simple interest on ${savings.balance:.2f} at {annual_rate*100}% for 1 year: ${simple_interest:.2f}")

    new_balance = InterestCalculator.apply_annual_interest(savings.balance, annual_rate)
    print(f"Bob's balance after 3% annual interest: ${new_balance:.2f}\n")

    # Transfers
    print("=== Transfers ===")
    TransactionManager.transfer(checking, savings, 100.0, "Transfer to savings")
    print(f"Alice transfers $100 to Bob")
    print(f"Alice's new balance: ${checking.balance:.2f}")
    print(f"Bob's new balance: ${savings.balance:.2f}\n")

    # Account information
    print("=== Account Information ===")
    alice_info = checking.get_account_info("1234")
    print(f"Alice's account: {alice_info}")
    bob_info = savings.get_account_info("5678")
    print(f"Bob's account: {bob_info}\n")

    # Transaction history
    print("=== Transaction History ===")
    print(f"Alice's transactions:")
    for tx in checking.get_transaction_history("1234"):
        print(f"  - {tx['type'].capitalize()}: ${tx['amount']:.2f} ({tx['description']})")

    print(f"\nBob's transactions:")
    for tx in savings.get_transaction_history("5678"):
        print(f"  - {tx['type'].capitalize()}: ${tx['amount']:.2f} ({tx['description']})")


if __name__ == "__main__":
    demo_banking_system()
