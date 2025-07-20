# budget_tracker.py

import json
import os
from pathlib import Path
from apps.budget_app.transaction import Transaction # Import the Transaction class
from colorama import Fore, Style
from collections import defaultdict # Useful for grouping

DATA_FILE = 'transactions.json' # File to store transaction data

def save_transactions_to_file(transactions_list):
    """Saves a list of Transaction objects to a JSON file."""
    try:
        # Convert Transaction objects to dictionaries before saving
        with open(DATA_FILE, 'w') as f:
            json.dump([t.to_dict() for t in transactions_list], f, indent=4)
        print(f"{Fore.GREEN}✓ Transactions saved successfully to '{DATA_FILE}'{Style.RESET_ALL}")
        return True
    except IOError as e:
        print(f"{Fore.RED}✗ Error saving transactions: {e}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}✗ An unexpected error occurred while saving: {e}{Style.RESET_ALL}")
        return False

def load_transactions_from_file():
    """Loads a list of Transaction objects from a JSON file."""
    if not Path(DATA_FILE).exists():
        print(f"{Fore.YELLOW}⚠ No transactions file '{DATA_FILE}' found. Starting with an empty list.{Style.RESET_ALL}")
        return []
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        
        # Convert dictionaries back into Transaction objects
        transactions = [Transaction.from_dict(t_data) for t_data in data]
        print(f"{Fore.GREEN}✓ Loaded {len(transactions)} transactions from '{DATA_FILE}'{Style.RESET_ALL}")
        return transactions
    except json.JSONDecodeError:
        print(f"{Fore.RED}✗ Transactions file '{DATA_FILE}' is corrupted. Starting with an empty list.{Style.RESET_ALL}")
        return []
    except IOError as e:
        print(f"{Fore.RED}✗ Error loading transactions: {e}{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED}✗ An unexpected error occurred while loading: {e}{Style.RESET_ALL}")
        return []

class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self._load_initial_data()

    def _load_initial_data(self):
        """Loads transaction data when the manager is initialized."""
        self.transactions = load_transactions_from_file()
        # Sort transactions by date after loading
        self.transactions.sort(key=lambda t: t.date)

    def add_transaction(self, date_str, category, amount):
        """Adds a new transaction."""
        try:
            new_transaction = Transaction(date_str, category, amount)
            self.transactions.append(new_transaction)
            # Re-sort list after adding a new transaction
            self.transactions.sort(key=lambda t: t.date)
            print(f"{Fore.GREEN}✓ Transaction added successfully.{Style.RESET_ALL}")
            return True
        except ValueError as e:
            print(f"{Fore.RED}✗ Failed to add transaction: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}✗ An unexpected error occurred while adding transaction: {e}{Style.RESET_ALL}")
            return False

    def view_all_transactions(self):
        """Displays details of all transactions."""
        if not self.transactions:
            print(f"{Fore.YELLOW}No transactions recorded yet.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}═══ All Transactions ═══{Style.RESET_ALL}")
        for i, transaction in enumerate(self.transactions, 1):
            print(f"{i}.{transaction}")
        print(f"{Fore.CYAN}════════════════════════{Style.RESET_ALL}")

    def get_transactions_by_category(self):
        """Groups transactions by category and calculates totals for each."""
        if not self.transactions:
            print(f"{Fore.YELLOW}No transactions to categorize.{Style.RESET_ALL}")
            return

        category_totals = defaultdict(float)
        category_transactions = defaultdict(list)

        for t in self.transactions:
            category_totals[t.category] += t.amount
            category_transactions[t.category].append(t)
        
        print(f"\n{Fore.CYAN}═══ Transactions By Category ═══{Style.RESET_ALL}")
        for category in sorted(category_totals.keys()): # Sort categories alphabetically
            print(f"\n{Fore.BLUE}Category: {category} (Total: €{category_totals[category]:.2f}){Style.RESET_ALL}")
            for t in category_transactions[category]:
                print(f"  {t}")
        print(f"{Fore.CYAN}═══════════════════════════════{Style.RESET_ALL}")

    def calculate_total_expenses(self):
        """Calculates the total sum of all expenses (excluding 'Salary' category)."""
        if not self.transactions:
            print(f"{Fore.YELLOW}No transactions to calculate total expenses from.{Style.RESET_ALL}")
            return 0.0
        
        total_expense = sum(t.amount for t in self.transactions if t.category != 'Salary')
        total_income = sum(t.amount for t in self.transactions if t.category == 'Salary')

        print(f"\n{Fore.CYAN}═══ Financial Summary ═══{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Total Income: €{total_income:.2f}{Style.RESET_ALL}")
        print(f"{Fore.RED}Total Expenses: €{total_expense:.2f}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Net Balance: €{total_income - total_expense:.2f}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}═══════════════════════{Style.RESET_ALL}")
        return total_expense

    def save_data(self):
        """Wrapper to save all transactions to file."""
        return save_transactions_to_file(self.transactions)

    def load_data(self):
        """Wrapper to load all transactions from file."""
        loaded_transactions = load_transactions_from_file()
        if loaded_transactions is not None:
            self.transactions = loaded_transactions
            # Ensure loaded data is sorted
            self.transactions.sort(key=lambda t: t.date)
            return True
        return False