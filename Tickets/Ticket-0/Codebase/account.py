"""
Account module - manages bank accounts with PIN authentication and balance tracking.
"""


class BankAccount:
    """Represents a single bank account with PIN protection."""

    def __init__(self, account_id: str, pin: str, holder_name: str, initial_balance: float = 0.0):
        """
        Initialize a bank account.

        Args:
            account_id: Unique identifier for the account
            pin: 4-digit PIN for authentication
            holder_name: Name of account holder
            initial_balance: Starting balance (default: 0.0)

        Raises:
            ValueError: If PIN is not 4 digits or balance is negative
        """
        if not isinstance(pin, str) or len(pin) != 4 or not pin.isdigit():
            raise ValueError("PIN must be a 4-digit string")
        if initial_balance < 0:
            raise ValueError("Balance cannot be negative")

        self.account_id = account_id
        self._pin = pin
        self.holder_name = holder_name
        self.balance = initial_balance
        self.transaction_history = []

    def verify_pin(self, pin: str) -> bool:
        """Verify if the provided PIN is correct."""
        return pin == self._pin

    def deposit(self, amount: float, description: str = "Deposit") -> bool:
        """
        Record a deposit to the account.

        Args:
            amount: Amount to deposit
            description: Transaction description

        Returns:
            True if successful
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.balance += amount
        self.transaction_history.append(
            {"type": "deposit", "amount": amount, "description": description, "balance_after": self.balance}
        )
        return True

    def withdraw(self, amount: float, description: str = "Withdrawal") -> bool:
        """
        Record a withdrawal from the account.

        Args:
            amount: Amount to withdraw
            description: Transaction description

        Returns:
            True if successful

        Raises:
            ValueError: If insufficient funds or invalid amount
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError(f"Insufficient funds. Available: {self.balance}")

        self.balance -= amount
        self.transaction_history.append(
            {"type": "withdrawal", "amount": amount, "description": description, "balance_after": self.balance}
        )
        return True

    def get_balance(self, pin: str) -> float:
        """
        Get current balance (requires PIN authentication).

        Args:
            pin: Account PIN

        Returns:
            Current balance

        Raises:
            ValueError: If PIN is incorrect
        """
        if not self.verify_pin(pin):
            raise ValueError("Incorrect PIN")
        return self.balance

    def get_account_info(self, pin: str) -> dict:
        """
        Get account information (requires PIN authentication).

        Args:
            pin: Account PIN

        Returns:
            Account details

        Raises:
            ValueError: If PIN is incorrect
        """
        if not self.verify_pin(pin):
            raise ValueError("Incorrect PIN")

        return {
            "account_id": self.account_id,
            "holder_name": self.holder_name,
            "balance": self.balance,
            "transactions": len(self.transaction_history),
        }

    def get_transaction_history(self, pin: str) -> list:
        """
        Get transaction history (requires PIN authentication).

        Args:
            pin: Account PIN

        Returns:
            List of transactions

        Raises:
            ValueError: If PIN is incorrect
        """
        if not self.verify_pin(pin):
            raise ValueError("Incorrect PIN")
        return self.transaction_history.copy()
