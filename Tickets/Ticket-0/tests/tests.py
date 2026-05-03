from pathlib import Path
import sys

CODEBASE_DIR = Path(__file__).resolve().parent.parent / "Codebase"
sys.path.insert(0, str(CODEBASE_DIR))

from calculator import add, subtract, multiply, divide
from account import BankAccount
from interest import InterestCalculator
from transactions import Transaction, TransactionManager
from bank import Bank


# ============================================================================
# Calculator Tests (Original)
# ============================================================================


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(3, 8) == -5


def test_multiply():
    assert multiply(6, 7) == 42
    assert multiply(-2, 5) == -10


def test_divide():
    assert divide(20, 5) == 4
    assert divide(7, 2) == 3.5


def test_divide_by_zero():
    try:
        divide(1, 0)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Cannot divide by zero"


# ============================================================================
# Account Tests
# ============================================================================


def test_account_creation():
    account = BankAccount("ACC001", "1234", "John Doe", 1000.0)
    assert account.account_id == "ACC001"
    assert account.holder_name == "John Doe"
    assert account.balance == 1000.0


def test_account_invalid_pin():
    try:
        BankAccount("ACC001", "123", "John", 100)  # PIN too short
        assert False, "Expected ValueError"
    except ValueError:
        pass

    try:
        BankAccount("ACC001", "12345", "John", 100)  # PIN too long
        assert False, "Expected ValueError"
    except ValueError:
        pass

    try:
        BankAccount("ACC001", "abcd", "John", 100)  # PIN not digits
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_account_negative_balance():
    try:
        BankAccount("ACC001", "1234", "John", -100)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_pin_verification():
    account = BankAccount("ACC001", "1234", "John", 100)
    assert account.verify_pin("1234") is True
    assert account.verify_pin("5678") is False


def test_deposit():
    account = BankAccount("ACC001", "1234", "John", 100.0)
    account.deposit(50.0, "Initial deposit")
    assert account.balance == 150.0
    assert len(account.transaction_history) == 1


def test_deposit_invalid_amount():
    account = BankAccount("ACC001", "1234", "John", 100.0)
    try:
        account.deposit(-50, "Bad deposit")
        assert False, "Expected ValueError"
    except ValueError:
        pass

    try:
        account.deposit(0, "Zero deposit")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_withdraw():
    account = BankAccount("ACC001", "1234", "John", 100.0)
    account.withdraw(30.0, "ATM withdrawal")
    assert account.balance == 70.0
    assert len(account.transaction_history) == 1


def test_withdraw_insufficient_funds():
    account = BankAccount("ACC001", "1234", "John", 100.0)
    try:
        account.withdraw(150.0, "Overdraft")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Insufficient funds" in str(exc)


def test_withdraw_invalid_amount():
    account = BankAccount("ACC001", "1234", "John", 100.0)
    try:
        account.withdraw(-50, "Bad withdrawal")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_get_balance_requires_pin():
    account = BankAccount("ACC001", "1234", "John", 100.0)
    assert account.get_balance("1234") == 100.0

    try:
        account.get_balance("9999")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Incorrect PIN" in str(exc)


def test_get_account_info():
    account = BankAccount("ACC001", "1234", "John", 100.0)
    account.deposit(50.0)
    info = account.get_account_info("1234")
    assert info["account_id"] == "ACC001"
    assert info["holder_name"] == "John"
    assert info["balance"] == 150.0
    assert info["transactions"] == 1


def test_transaction_history():
    account = BankAccount("ACC001", "1234", "John", 100.0)
    account.deposit(50.0, "Deposit 1")
    account.withdraw(20.0, "Withdrawal 1")
    account.deposit(30.0, "Deposit 2")

    history = account.get_transaction_history("1234")
    assert len(history) == 3
    assert history[0]["type"] == "deposit"
    assert history[1]["type"] == "withdrawal"
    assert history[2]["type"] == "deposit"


# ============================================================================
# Interest Calculator Tests
# ============================================================================


def test_simple_interest():
    # $1000 at 5% for 1 year = $50
    interest = InterestCalculator.simple_interest(1000, 0.05, 1)
    assert interest == 50.0

    # $1000 at 5% for 2 years = $100
    interest = InterestCalculator.simple_interest(1000, 0.05, 2)
    assert interest == 100.0


def test_simple_interest_negative_values():
    try:
        InterestCalculator.simple_interest(-1000, 0.05, 1)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_apply_annual_interest():
    # $1000 at 3% = $1030
    new_balance = InterestCalculator.apply_annual_interest(1000, 0.03)
    assert new_balance == 1030.0

    # $500 at 5% = $525
    new_balance = InterestCalculator.apply_annual_interest(500, 0.05)
    assert new_balance == 525.0


def test_apply_annual_interest_negative_values():
    try:
        InterestCalculator.apply_annual_interest(-100, 0.05)
        assert False, "Expected ValueError"
    except ValueError:
        pass


# ============================================================================
# Transaction Tests
# ============================================================================


def test_transaction_creation():
    tx = Transaction("deposit", 100.0)
    assert tx.transaction_type == "deposit"
    assert tx.amount == 100.0


def test_transaction_invalid_type():
    try:
        Transaction("invalid_type", 100.0)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_transaction_invalid_amount():
    try:
        Transaction("deposit", -50)
        assert False, "Expected ValueError"
    except ValueError:
        pass

    try:
        Transaction("deposit", 0)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_transfer():
    account1 = BankAccount("ACC001", "1234", "Alice", 500.0)
    account2 = BankAccount("ACC002", "5678", "Bob", 100.0)

    TransactionManager.transfer(account1, account2, 100.0, "Transfer")

    assert account1.balance == 400.0
    assert account2.balance == 200.0


def test_transfer_insufficient_funds():
    account1 = BankAccount("ACC001", "1234", "Alice", 50.0)
    account2 = BankAccount("ACC002", "5678", "Bob", 100.0)

    try:
        TransactionManager.transfer(account1, account2, 100.0)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Insufficient funds" in str(exc)


def test_transfer_creates_history():
    account1 = BankAccount("ACC001", "1234", "Alice", 500.0)
    account2 = BankAccount("ACC002", "5678", "Bob", 100.0)

    TransactionManager.transfer(account1, account2, 100.0)

    assert len(account1.transaction_history) == 1
    assert len(account2.transaction_history) == 1


def test_validate_transaction():
    assert TransactionManager.validate_transaction("deposit", 100) is True
    assert TransactionManager.validate_transaction("withdrawal", 50) is True
    assert TransactionManager.validate_transaction("transfer", 75) is True
    assert TransactionManager.validate_transaction("invalid", 100) is False
    assert TransactionManager.validate_transaction("deposit", -50) is False


# ============================================================================
# Bank Tests
# ============================================================================


def test_bank_creation():
    bank = Bank("TestBank")
    assert bank.bank_name == "TestBank"
    assert len(bank.list_accounts()) == 0


def test_create_account():
    bank = Bank("TestBank")
    account = bank.create_account("ACC001", "1234", "John", 100.0)
    assert account.holder_name == "John"
    assert bank.account_exists("ACC001") is True


def test_create_duplicate_account():
    bank = Bank("TestBank")
    bank.create_account("ACC001", "1234", "John", 100.0)

    try:
        bank.create_account("ACC001", "5678", "Jane", 200.0)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "already exists" in str(exc)


def test_get_account():
    bank = Bank("TestBank")
    account = bank.create_account("ACC001", "1234", "John", 100.0)
    retrieved = bank.get_account("ACC001")
    assert retrieved.account_id == account.account_id


def test_get_nonexistent_account():
    bank = Bank("TestBank")
    try:
        bank.get_account("ACC999")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "not found" in str(exc)


def test_list_accounts():
    bank = Bank("TestBank")
    bank.create_account("ACC001", "1234", "John", 100.0)
    bank.create_account("ACC002", "5678", "Jane", 200.0)
    accounts = bank.list_accounts()
    assert "ACC001" in accounts
    assert "ACC002" in accounts
    assert len(accounts) == 2


def test_bank_workflow():
    """Test a complete banking workflow."""
    bank = Bank("SimpleBank")

    # Create accounts
    checking = bank.create_account("CHK001", "1111", "Alice", 1000.0)
    savings = bank.create_account("SAV001", "2222", "Bob", 500.0)

    # Deposits
    checking.deposit(250.0)
    savings.deposit(100.0)

    # Withdrawals
    checking.withdraw(150.0)
    savings.withdraw(50.0)

    # Transfer
    TransactionManager.transfer(checking, savings, 100.0)

    # Verify balances
    assert checking.balance == 1000.0  # 1000 + 250 - 150 - 100
    assert savings.balance == 550.0  # 500 + 100 - 50 + 100

    # Apply interest
    savings.balance = InterestCalculator.apply_annual_interest(savings.balance, 0.03)
    assert savings.balance == 550.0 * 1.03

    # Verify transactions tracked
    assert len(checking.transaction_history) == 3  # deposit, withdraw, transfer
    assert len(savings.transaction_history) == 3  # deposit, withdraw, transfer
