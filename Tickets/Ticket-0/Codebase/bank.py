"""
Bank module - main banking system managing multiple accounts.
"""

from account import BankAccount


class Bank:
    """Represents a bank managing multiple accounts."""

    def __init__(self, bank_name: str):
        """
        Initialize a bank.

        Args:
            bank_name: Name of the bank
        """
        self.bank_name = bank_name
        self.accounts = {}

    def create_account(self, account_id: str, pin: str, holder_name: str, initial_balance: float = 0.0) -> BankAccount:
        """
        Create a new bank account.

        Args:
            account_id: Unique account identifier
            pin: 4-digit PIN
            holder_name: Name of account holder
            initial_balance: Starting balance

        Returns:
            Created BankAccount object

        Raises:
            ValueError: If account already exists
        """
        if account_id in self.accounts:
            raise ValueError(f"Account {account_id} already exists")

        account = BankAccount(account_id, pin, holder_name, initial_balance)
        self.accounts[account_id] = account
        return account

    def get_account(self, account_id: str) -> BankAccount:
        """
        Retrieve an account by ID.

        Args:
            account_id: Account identifier

        Returns:
            BankAccount object

        Raises:
            ValueError: If account not found
        """
        if account_id not in self.accounts:
            raise ValueError(f"Account {account_id} not found")
        return self.accounts[account_id]

    def list_accounts(self) -> list:
        """Get list of all account IDs."""
        return list(self.accounts.keys())

    def account_exists(self, account_id: str) -> bool:
        """Check if an account exists."""
        return account_id in self.accounts
