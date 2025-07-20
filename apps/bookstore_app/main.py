# bookstore_app/main.py
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
    print(f"{Fore.YELLOW}           Bookstore Inventory System 📚           {Style.RESET_ALL}")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.BLUE}1.{Style.RESET_ALL} Add New Book")
    print(f"{Fore.BLUE}2.{Style.RESET_ALL} View All Books")
    print(f"{Fore.BLUE}3.{Style.RESET_ALL} Search Books") 
    print(f"{Fore.BLUE}4.{Style.RESET_ALL} Update Book Details") 
    print(f"{Fore.BLUE}5.{Style.RESET_ALL} Delete Book") 
    print(f"{Fore.BLUE}6.{Style.RESET_ALL} Save Inventory")
    print(f"{Fore.BLUE}7.{Style.RESET_ALL} Load Inventory")
    print(f"{Fore.BLUE}8.{Style.RESET_ALL} Back to Main Menu")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")

def _select_book_from_results(found_books):
    """
    Helper function to display a list of books and allow the user to select one.
    Returns the selected Book object or None if cancelled/invalid selection.
    """
    if not found_books:
        print(f"{Fore.YELLOW}No books found matching your criteria.{Style.RESET_ALL}")
        return None

    print(f"\n{Fore.CYAN}--- Found Books ---{Style.RESET_ALL}")
    for i, book in enumerate(found_books, 1):
        print(f"{Fore.BLUE}{i}.{Style.RESET_ALL} {book}")
    print(f"-------------------")

    while True:
        choice_str = get_valid_input(
            "Enter the number of the book to select (or 'c' to cancel):",
            validator=lambda x: x if (x.isdigit() and 1 <= int(x) <= len(found_books)) or x.lower() == 'c' else (_ for _ in ()).throw(ValueError("Invalid number or 'c'."))
        )
        if choice_str is None or choice_str.lower() == 'c':
            print(f"{Fore.BLUE}Selection cancelled.{Style.RESET_ALL}")
            return None
        
        try:
            choice_index = int(choice_str) - 1
            return found_books[choice_index]
        except (ValueError, IndexError): # Should ideally be caught by validator, but as a fallback
            print(f"{Fore.RED}Invalid selection. Please enter a valid number or 'c'.{Style.RESET_ALL}")


def handle_search_books(manager):
    """Handles the search books functionality."""
    print(f"\n{Fore.CYAN}═══ Search Books ═══{Style.RESET_ALL}")
    search_term = get_valid_input("Enter title or author to search for:")
    if search_term is None:
        return # User cancelled

    found_books = manager.find_books(search_term)

    if not found_books:
        print(f"{Fore.YELLOW}No books found matching '{search_term}'.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.GREEN}Found {len(found_books)} book(s) matching '{search_term}':{Style.RESET_ALL}")
        for i, book in enumerate(found_books, 1):
            print(f" {i}. {book}")


def handle_update_book(manager):
    """Handles the update book details functionality."""
    print(f"\n{Fore.CYAN}═══ Update Book Details ═══{Style.RESET_ALL}")
    search_term = get_valid_input("Enter title or author of the book to update:")
    if search_term is None: return

    found_books = manager.find_books(search_term)
    if not found_books:
        print(f"{Fore.YELLOW}No book found matching '{search_term}'. Cannot update.{Style.RESET_ALL}")
        return

    book_to_update = _select_book_from_results(found_books)
    if book_to_update is None: return # User cancelled selection

    print(f"\n{Fore.CYAN}--- Updating: {book_to_update.title} by {book_to_update.author} ---{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Enter new values or press Enter to keep current value.{Style.RESET_ALL}")

    new_title = get_valid_input(f"New Title (current: {book_to_update.title}):", allow_empty=True, 
                                validator=lambda x: Book._validate_string_input(x, "Title") if x.strip() else x)
    if new_title is None: return # User cancelled
    if not new_title.strip(): new_title = None # Treat empty input as "keep current"

    new_author = get_valid_input(f"New Author (current: {book_to_update.author}):", allow_empty=True, 
                                 validator=lambda x: Book._validate_string_input(x, "Author") if x.strip() else x)
    if new_author is None: return # User cancelled
    if not new_author.strip(): new_author = None

    new_price_str = get_valid_input(f"New Price (current: €{book_to_update.price:.2f}):", allow_empty=True, 
                                    validator=lambda x: Book._validate_price(float(x)) if x.strip() else x,
                                    error_message=f"{Fore.RED}Invalid price. Must be a positive number.{Style.RESET_ALL}")
    if new_price_str is None: return # User cancelled
    new_price = float(new_price_str) if new_price_str.strip() else None

    new_stock_str = get_valid_input(f"New Stock (current: {book_to_update.stock} units):", allow_empty=True, 
                                    validator=lambda x: Book._validate_stock(int(x)) if x.strip() else x,
                                    error_message=f"{Fore.RED}Invalid stock. Must be a non-negative whole number.{Style.RESET_ALL}")
    if new_stock_str is None: return # User cancelled
    new_stock = int(new_stock_str) if new_stock_str.strip() else None

    manager.update_book(book_to_update, new_title, new_author, new_price, new_stock)


def handle_delete_book(manager):
    """Handles the delete book functionality."""
    print(f"\n{Fore.CYAN}═══ Delete Book ═══{Style.RESET_ALL}")
    search_term = get_valid_input("Enter title or author of the book to delete:")
    if search_term is None: return

    found_books = manager.find_books(search_term)
    if not found_books:
        print(f"{Fore.YELLOW}No book found matching '{search_term}'. Cannot delete.{Style.RESET_ALL}")
        return

    book_to_delete = _select_book_from_results(found_books)
    if book_to_delete is None: return # User cancelled selection

    confirm = get_valid_input(
        f"{Fore.YELLOW}Are you sure you want to delete '{book_to_delete.title}' by {book_to_delete.author}? (yes/no):{Style.RESET_ALL} ",
        validator=lambda x: x.lower() if x.lower() in ['yes', 'no'] else (_ for _ in ()).throw(ValueError("Invalid input. Please enter 'yes' or 'no'.")))
    
    if confirm == 'yes':
        manager.delete_book(book_to_delete)
    else:
        print(f"{Fore.BLUE}Deletion cancelled.{Style.RESET_ALL}")


def run_bookstore_app():
    setup_app_colors() # Initialize colorama
    manager = InventoryManager() # Automatically loads data on init

    while True:
        display_main_menu()
        
        choice = get_valid_input("Enter your choice (1-8):", 
                                 validator=lambda x: x if x in ['1','2','3','4','5','6','7','8'] 
                                 else (_ for _ in ()).throw(ValueError("Invalid choice. Please enter a number between 1 and 8.")),
                                 error_message=f"{Fore.RED}Invalid choice. Please enter a number between 1 and 8.{Style.RESET_ALL}")
        
        if choice is None: # User cancelled menu input
            continue 

        if choice == '1': # Add New Book
            print(f"\n{Fore.CYAN}═══ Add New Book ═══{Style.RESET_ALL}")
            title = get_valid_input("Enter book title:", 
                                    validator=lambda x: Book._validate_string_input(x, "Title"),
                                    error_message=f"{Fore.RED}Title cannot be empty.{Style.RESET_ALL}")
            if title is None: continue
            
            author = get_valid_input("Enter author's name:", 
                                    validator=lambda x: Book._validate_string_input(x, "Author"),
                                    error_message=f"{Fore.RED}Author's name cannot be empty.{Style.RESET_ALL}")
            if author is None: continue
            
            # Pass type_func and error_message for robust input handling
            price = get_valid_input("Enter price (e.g., 29.99):", 
                                    type_func=float, 
                                    validator=Book._validate_price,
                                    error_message=f"{Fore.RED}Invalid price. Must be a positive number.{Style.RESET_ALL}")
            if price is None: continue
            
            stock = get_valid_input("Enter stock quantity:", 
                                    type_func=int, 
                                    validator=Book._validate_stock,
                                    error_message=f"{Fore.RED}Invalid stock. Must be a non-negative whole number.{Style.RESET_ALL}")
            if stock is None: continue

            manager.add_book(title, author, price, stock)
        
        elif choice == '2': # View All Books
            manager.view_all_books()
        
        elif choice == '3': # Search Books
            handle_search_books(manager)
            
        elif choice == '4': # Update Book Details
            handle_update_book(manager)

        elif choice == '5': # Delete Book
            handle_delete_book(manager)

        elif choice == '6': # Save Inventory
            manager.save_data()
        
        elif choice == '7': # Load Inventory
            if manager.books: # Only ask if there's data in memory
                confirm = get_valid_input(
                    f"{Fore.YELLOW}Warning: Loading new data will overwrite current unsaved changes. Proceed? (yes/no):{Style.RESET_ALL} ",
                    validator=lambda x: x.lower() if x.lower() in ['yes', 'no'] else (_ for _ in ()).throw(ValueError("Invalid input. Please enter 'yes' or 'no'.")),
                    error_message=f"{Fore.RED}Invalid input. Please enter 'yes' or 'no'.{Style.RESET_ALL}")
                if confirm != 'yes':
                    print(f"{Fore.BLUE}Loading cancelled.{Style.RESET_ALL}")
                    continue
            
            manager.load_data() 
        
        elif choice == '8': # Back to Main Menu
            # Optionally, ask to save before returning to main app menu if changes exist
            print(f"{Fore.BLUE}Returning to main application menu.{Style.RESET_ALL}")
            break
