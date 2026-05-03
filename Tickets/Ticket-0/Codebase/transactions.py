"""
Transactions module - manages deposits, withdrawals, and transfers between accounts.
"""


class Transaction:
    """Represents a single financial transaction."""

    TRANSACTION_TYPES = {"deposit", "withdrawal", "transfer"}

    def __init__(self, transaction_type: str, amount: float, description: str = ""):
        """
        Initialize a transaction.

        Args:
            transaction_type: Type of transaction (deposit, withdrawal, transfer)
            amount: Transaction amount
            description: Optional transaction description

        Raises:
            ValueError: If type is invalid or amount is not positive
        """
        if transaction_type not in self.TRANSACTION_TYPES:
            raise ValueError(f"Invalid transaction type: {transaction_type}")
        if amount <= 0:
            raise ValueError("Transaction amount must be positive")

        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description or transaction_type.capitalize()

    def to_dict(self) -> dict:
        """Convert transaction to dictionary."""
        return {
            "type": self.transaction_type,
            "amount": self.amount,
            "description": self.description,
        }


class TransactionManager:
    """Manages transactions between accounts."""

    @staticmethod
    def transfer(from_account, to_account, amount: float, description: str = "Transfer") -> bool:
        """
        Transfer funds between two accounts.

        Args:
            from_account: Source account (BankAccount object)
            to_account: Destination account (BankAccount object)
            amount: Amount to transfer
            description: Transaction description

        Returns:
            True if successful

        Raises:
            ValueError: If transfer fails
        """
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        # Check sufficient funds
        if from_account.balance < amount:
            raise ValueError(f"Insufficient funds in source account. Available: {from_account.balance}")

        # Execute withdrawal and deposit
        from_account.withdraw(amount, f"{description} to {to_account.account_id}")
        to_account.deposit(amount, f"{description} from {from_account.account_id}")

        return True

    @staticmethod
    def validate_transaction(transaction_type: str, amount: float) -> bool:
        """
        Validate transaction parameters.

        Args:
            transaction_type: Type of transaction
            amount: Transaction amount

        Returns:
            True if valid
        """
        if transaction_type not in Transaction.TRANSACTION_TYPES:
            return False
        return amount > 0
