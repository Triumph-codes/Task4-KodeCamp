# main.py
import sys
from os.path import dirname, join, abspath

# Add project root to Python path
project_root = abspath(join(dirname(dirname(dirname(__file__)))))
sys.path.insert(0, project_root)

try:
    from shared.utils import setup_app_colors, get_valid_input
    from apps.bookstore_app.book import Book
    from apps.bookstore_app.inventory import InventoryManager
except ImportError as e:
    print(f"Import Error: {e}")
    raise

from colorama import Fore, Style

def display_main_menu():
    """Displays the main menu options for the Bookstore Inventory System."""
    print(f"\n{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}          Bookstore Inventory System 📚          {Style.RESET_ALL}")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.BLUE}1.{Style.RESET_ALL} Add New Book")
    print(f"{Fore.BLUE}2.{Style.RESET_ALL} View All Books")
    print(f"{Fore.BLUE}3.{Style.RESET_ALL} Search Books (Future Feature on Branch)")
    print(f"{Fore.BLUE}4.{Style.RESET_ALL} Update Book Details (Future Feature)")
    print(f"{Fore.BLUE}5.{Style.RESET_ALL} Delete Book (Future Feature)")
    print(f"{Fore.BLUE}6.{Style.RESET_ALL} Save Inventory")
    print(f"{Fore.BLUE}7.{Style.RESET_ALL} Load Inventory")
    print(f"{Fore.BLUE}8.{Style.RESET_ALL} Back to Main Menu")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")

def run_bookstore_app():
    setup_app_colors() # Initialize colorama
    manager = InventoryManager() # Automatically loads data on init

    while True:
        display_main_menu()
        
        choice = get_valid_input("Enter your choice (1-8):", 
                                 validator=lambda x: x if x in ['1','2','3','4','5','6','7','8'] 
                                 else (_ for _ in ()).throw(ValueError("Invalid choice. Please enter a number between 1 and 8.")))
        
        if choice is None: # User cancelled menu input
            continue 

        if choice == '1': # Add New Book
            print(f"\n{Fore.CYAN}═══ Add New Book ═══{Style.RESET_ALL}")
            title = get_valid_input("Enter book title:", validator=lambda x: Book._validate_string_input(x, "Title"))
            if title is None: continue
            # Note: We pass a dummy field name "Author" to the validator since it's a general string validator.
            author = get_valid_input("Enter author's name:", validator=lambda x: Book._validate_string_input(x, "Author"))
            if author is None: continue
            price = get_valid_input("Enter price (e.g., 29.99):", validator=Book._validate_price)
            if price is None: continue
            stock = get_valid_input("Enter stock quantity:", validator=Book._validate_stock)
            if stock is None: continue

            manager.add_book(title, author, price, stock)
        
        elif choice == '2': # View All Books
            manager.view_all_books()
        
        elif choice == '3': # Search Books (Placeholder for future feature)
            print(f"{Fore.YELLOW}This feature will be implemented in a 'feature-search' branch.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Stay tuned for the next step!{Style.RESET_ALL}")
            
        elif choice == '4': # Update Book Details (Placeholder)
            print(f"{Fore.YELLOW}This feature will be implemented soon.{Style.RESET_ALL}")

        elif choice == '5': # Delete Book (Placeholder)
            print(f"{Fore.YELLOW}This feature will be implemented soon.{Style.RESET_ALL}")

        elif choice == '6': # Save Inventory
            manager.save_data()
        
        elif choice == '7': # Load Inventory
            # Ask for confirmation before overwriting in-memory data
            if manager.books: # Only ask if there's data in memory
                confirm = get_valid_input(
                    f"{Fore.YELLOW}Warning: Loading new data will overwrite current unsaved changes. Proceed? (yes/no):{Style.RESET_ALL} ",
                    validator=lambda x: x.lower() if x.lower() in ['yes', 'no'] else (_ for _ in ()).throw(ValueError("Invalid input. Please enter 'yes' or 'no'.")))
                if confirm != 'yes':
                    print(f"{Fore.BLUE}Loading cancelled.{Style.RESET_ALL}")
                    continue
            
            manager.load_data() # This will reassign manager.books internally
        
        elif choice == '8': # Exit Application
            confirm_exit = get_valid_input(
                f"{Fore.YELLOW}Exit without saving current changes? (yes/no):{Style.RESET_ALL} ",
                validator=lambda x: x.lower() if x.lower() in ['yes', 'no'] else (_ for _ in ()).throw(ValueError("Invalid input. Please enter 'yes' or 'no'.")))
            if confirm_exit == 'yes':
                print(f"{Fore.GREEN}Goodbye from Bookstore App! 📚{Style.RESET_ALL}")
                break
            elif confirm_exit is None: # User cancelled exit, stay in app
                print(f"{Fore.BLUE}Exit cancelled.{Style.RESET_ALL}")
                continue
            else:
                print(f"{Fore.BLUE}Exit cancelled. Returning to main menu.{Style.RESET_ALL}")

