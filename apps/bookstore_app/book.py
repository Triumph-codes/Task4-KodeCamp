# book.py

from colorama import Fore, Style
import math # Will be used for price rounding if needed

class Book:
    def __init__(self, title, author, price, stock):
        self.title = self._validate_string_input(title, "Title")
        self.author = self._validate_string_input(author, "Author")
        self.price = self._validate_price(price)
        self.stock = self._validate_stock(stock)

    @staticmethod
    def _validate_string_input(value, field_name):
        """Validates if a string input is not empty and is a string."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return value.strip()

    @staticmethod
    def _validate_price(price):
        """Validates and rounds the book price."""
        try:
            price = float(price)
        except (ValueError, TypeError):
            raise ValueError("Price must be a number.")
        if price <= 0:
            raise ValueError("Price must be positive.")
        return round(price, 2) # Round to 2 decimal places

    @staticmethod
    def _validate_stock(stock):
        """Validates the book stock (quantity)."""
        try:
            stock = int(stock)
        except (ValueError, TypeError):
            raise ValueError("Stock must be a whole number.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        return stock

    def display_info(self):
        """Prints the book's details."""
        print(f"{Fore.CYAN}Title:{Style.RESET_ALL} {self.title}")
        print(f"{Fore.CYAN}Author:{Style.RESET_ALL} {self.author}")
        print(f"{Fore.CYAN}Price:{Style.RESET_ALL} €{self.price:.2f}")
        print(f"{Fore.CYAN}Stock:{Style.RESET_ALL} {self.stock} units")

    def __str__(self):
        """String representation for printing the object directly."""
        return (f"{Fore.YELLOW}{self.title}{Style.RESET_ALL} by {self.author} - "
                f"€{self.price:.2f} ({self.stock} in stock)")

    def to_dict(self):
        """Converts the Book object to a dictionary for JSON serialization."""
        return {
            "title": self.title,
            "author": self.author,
            "price": self.price,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Book object from a dictionary loaded from JSON."""
        return cls(data["title"], data["author"], data["price"], data["stock"])