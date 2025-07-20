# main.py (for Personal Budget Tracker)
# budget_app/main.py
import sys
from os.path import dirname, join, abspath

# 1. Add project root to Python path
project_root = abspath(join(dirname(dirname(dirname(__file__)))))
sys.path.insert(0, project_root)

# 2. Import shared utilities first
from shared.utils import setup_app_colors, get_valid_input

# 3. Import from within budget_app using absolute paths
from apps.budget_app.transaction import Transaction
from apps.budget_app.budget_tracker import BudgetTracker

# 4. Other imports
from colorama import Fore, Style

def display_main_menu():
    """Displays the main menu options for the Personal Budget Tracker."""
    print(f"\n{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}          Personal Budget Tracker 💰          {Style.RESET_ALL}")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.BLUE}1.{Style.RESET_ALL} Add New Transaction")
    print(f"{Fore.BLUE}2.{Style.RESET_ALL} View All Transactions")
    print(f"{Fore.BLUE}3.{Style.RESET_ALL} View Transactions by Category")
    print(f"{Fore.BLUE}4.{Style.RESET_ALL} Calculate Total Expenses")
    print(f"{Fore.BLUE}5.{Style.RESET_ALL} Save Transactions")
    print(f"{Fore.BLUE}6.{Style.RESET_ALL} Load Transactions")
    print(f"{Fore.BLUE}7.{Style.RESET_ALL} Back to Main Menu")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")

def get_transaction_details():
    """Interactively gets transaction details from the user."""
    print(f"\n{Fore.CYAN}--- Enter New Transaction Details ---{Style.RESET_ALL}")
    
    # Get Date
    date_str = get_valid_input("Enter date (YYYY-MM-DD, e.g., 2023-10-27):", validator=Transaction._validate_date)
    if date_str is None: return None # User cancelled

    # Get Category
    print(f"Available categories: {Fore.BLUE}{', '.join(Transaction.VALID_CATEGORIES)}{Style.RESET_ALL}")
    category = get_valid_input("Enter category:", validator=Transaction._validate_category)
    if category is None: return None # User cancelled

    # Get Amount
    amount = get_valid_input("Enter amount (e.g., 50.75):", validator=Transaction._validate_amount)
    if amount is None: return None # User cancelled

    # Convert date object back to string for passing to add_transaction
    return {
        'date': date_str.strftime("%Y-%m-%d"), # Keep as string for add_transaction, it re-validates
        'category': category,
        'amount': amount
    }

def run_budget_app():
    setup_app_colors() # Initialize colorama
    manager = BudgetTracker() # Automatically loads data on init

    while True:
        display_main_menu()
        
        choice = get_valid_input("Enter your choice (1-7):", 
                                 validator=lambda x: x if x in ['1','2','3','4','5','6','7'] 
                                 else (_ for _ in ()).throw(ValueError("Invalid choice. Please enter a number between 1 and 7.")))
        
        if choice is None: # User cancelled menu input
            continue 

        if choice == '1': # Add New Transaction
            transaction_details = get_transaction_details()
            if transaction_details is None: continue # User cancelled input process

            manager.add_transaction(
                transaction_details['date'], 
                transaction_details['category'], 
                transaction_details['amount']
            )
        
        elif choice == '2': # View All Transactions
            manager.view_all_transactions()
        
        elif choice == '3': # View Transactions by Category
            manager.get_transactions_by_category()

        elif choice == '4': # Calculate Total Expenses
            manager.calculate_total_expenses()

        elif choice == '5': # Save Transactions
            manager.save_data()
        
        elif choice == '6': # Load Transactions
            if manager.transactions: # Only ask if there's data in memory
                confirm = get_valid_input(
                    f"{Fore.YELLOW}Warning: Loading new data will overwrite current unsaved changes. Proceed? (yes/no):{Style.RESET_ALL} ",
                    validator=lambda x: x.lower() if x.lower() in ['yes', 'no'] else (_ for _ in ()).throw(ValueError("Invalid input. Please enter 'yes' or 'no'.")))
                if confirm != 'yes':
                    print(f"{Fore.BLUE}Loading cancelled.{Style.RESET_ALL}")
                    continue
            
            manager.load_data() # This will reassign manager.transactions internally
        
        elif choice == '7': # Back to Main Menu
            print(f"{Fore.BLUE}Returning to main application menu.{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    print("Budget App Imports Working!")
    print(f"Utils imported from: {setup_app_colors.__module__}")
    print(f"Transaction imported from: {Transaction.__module__}")