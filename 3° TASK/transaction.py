# transaction.py

from datetime import datetime, date # Import datetime and date
from colorama import Fore, Style # For __str__ display

class Transaction:
    VALID_CATEGORIES = [
        'Food', 'Transport', 'Utilities', 'Rent', 'Entertainment',
        'Shopping', 'Salary', 'Groceries', 'Healthcare', 'Education',
        'Miscellaneous' # Added a general category
    ]

    def __init__(self, date_str, category, amount):
        self.date = self._validate_date(date_str)
        self.category = self._validate_category(category)
        self.amount = self._validate_amount(amount)

    @staticmethod
    def _validate_date(date_str):
        """Validates and converts a date string (YYYY-MM-DD) to a date object."""
        if not isinstance(date_str, str):
            raise ValueError("Date must be a string in YYYY-MM-DD format.")
        try:
            # Attempt to parse the date string
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD (e.g., 2023-10-27).")
        
        # Optional: Check if date is not in the future
        if parsed_date > date.today():
            raise ValueError("Date cannot be in the future.")
        return parsed_date

    @staticmethod
    def _validate_category(category):
        """Validates the transaction category."""
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category cannot be empty.")
        category = category.strip().capitalize() # Capitalize for consistency
        if category not in Transaction.VALID_CATEGORIES:
            raise ValueError(f"Invalid category: '{category}'. Choose from: {', '.join(Transaction.VALID_CATEGORIES)}.")
        return category

    @staticmethod
    def _validate_amount(amount):
        """Validates the transaction amount."""
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ValueError("Amount must be a number.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        return round(amount, 2) # Round to 2 decimal places for currency

    def __str__(self):
        """String representation for displaying a transaction."""
        amount_color = Fore.RED if self.category != 'Salary' else Fore.GREEN # Different color for income
        return (
            f"  {Fore.CYAN}Date:{Style.RESET_ALL} {self.date.strftime('%Y-%m-%d')} | "
            f"{Fore.CYAN}Category:{Style.RESET_ALL} {Fore.BLUE}{self.category}{Style.RESET_ALL} | "
            f"{Fore.CYAN}Amount:{Style.RESET_ALL} {amount_color}€{self.amount:.2f}{Style.RESET_ALL}"
        )

    def to_dict(self):
        """Converts the Transaction object to a dictionary for JSON serialization."""
        return {
            "date": self.date.strftime("%Y-%m-%d"), # Convert date object back to string
            "category": self.category,
            "amount": self.amount
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Transaction object from a dictionary loaded from JSON."""
        # Note: from_dict re-validates data, which is good for robustness
        return cls(data["date"], data["category"], data["amount"])