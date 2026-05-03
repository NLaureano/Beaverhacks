"""
Interest module - handles interest calculations for savings accounts.
"""

from calculator import multiply, divide


class InterestCalculator:
    """Calculates compound and simple interest on account balances."""

    @staticmethod
    def simple_interest(principal: float, rate: float, time_years: float) -> float:
        """
        Calculate simple interest.

        Formula: Interest = Principal × Rate × Time

        Args:
            principal: Starting balance
            rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
            time_years: Time period in years

        Returns:
            Interest amount
        """
        if principal < 0 or rate < 0 or time_years < 0:
            raise ValueError("Principal, rate, and time must be non-negative")

        return multiply(multiply(principal, rate), time_years)

    @staticmethod
    def compound_interest(principal: float, rate: float, compounds_per_year: int, time_years: float) -> float:
        """
        Calculate compound interest total (principal + interest).

        Formula: A = P(1 + r/n)^(nt)

        Args:
            principal: Starting balance
            rate: Annual interest rate (as decimal)
            compounds_per_year: Compounding frequency (1=annual, 4=quarterly, 12=monthly, 365=daily)
            time_years: Time period in years

        Returns:
            Total amount (principal + interest)
        """
        if principal < 0 or rate < 0 or compounds_per_year <= 0 or time_years < 0:
            raise ValueError("Invalid parameters for compound interest")

        # Calculate rate per period: r/n
        rate_per_period = divide(rate, compounds_per_year)

        # Calculate 1 + rate_per_period
        growth_factor = 1 + rate_per_period

        # Calculate number of periods: n*t
        num_periods = multiply(compounds_per_year, time_years)

        # Calculate (1 + r/n)^(nt) - approximation with multiple multiplications
        result = principal
        for _ in range(int(num_periods)):
            result = multiply(result, growth_factor)

        return result

    @staticmethod
    def apply_annual_interest(balance: float, rate: float) -> float:
        """
        Apply annual interest once to a balance.

        Args:
            balance: Current balance
            rate: Annual interest rate (as decimal)

        Returns:
            New balance after interest
        """
        if balance < 0 or rate < 0:
            raise ValueError("Balance and rate must be non-negative")

        interest_earned = multiply(balance, rate)
        return balance + interest_earned
