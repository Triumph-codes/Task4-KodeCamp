# apps/bookstore_app/inventory.py

import json
import os
# import math # This import is not used and can be removed
from pathlib import Path
from apps.bookstore_app.book import Book # Import the Book class
from colorama import Fore, Style

DATA_FILE = 'books.json' # File to store book inventory

def save_books_to_file(books_list):
    """Saves a list of Book objects to a JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump([b.to_dict() for b in books_list], f, indent=4)
        print(f"{Fore.GREEN}✓ Inventory saved successfully to '{DATA_FILE}'{Style.RESET_ALL}")
        return True
    except IOError as e:
        print(f"{Fore.RED}✗ Error saving inventory: {e}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}✗ An unexpected error occurred while saving: {e}{Style.RESET_ALL}")
        return False

def load_books_from_file():
    """Loads a list of Book objects from a JSON file."""
    if not Path(DATA_FILE).exists():
        print(f"{Fore.YELLOW}⚠ No inventory file '{DATA_FILE}' found. Starting with an empty inventory.{Style.RESET_ALL}")
        return []
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        
        # Convert dictionaries back into Book objects
        books = [Book.from_dict(b_data) for b_data in data]
        print(f"{Fore.GREEN}✓ Loaded {len(books)} books from '{DATA_FILE}'{Style.RESET_ALL}")
        return books
    except json.JSONDecodeError:
        print(f"{Fore.RED}✗ Inventory file '{DATA_FILE}' is corrupted. Starting with an empty inventory.{Style.RESET_ALL}")
        return []
    except IOError as e:
        print(f"{Fore.RED}✗ Error loading inventory: {e}{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED}✗ An unexpected error occurred while loading: {e}{Style.RESET_ALL}")
        return []

class InventoryManager:
    def __init__(self):
        self.books = []
        self._load_initial_data()

    def _load_initial_data(self):
        """Loads book data when the manager is initialized."""
        self.books = load_books_from_file()

    def add_book(self, title, author, price, stock):
        """Adds a new book to the inventory."""
        try:
            # Check for exact duplicate (title and author) to prevent accidental double-entry
            if any(b.title.lower() == title.lower() and b.author.lower() == author.lower() for b in self.books):
                raise ValueError(f"Book '{title}' by {author} already exists in inventory.")
            
            new_book = Book(title, author, price, stock)
            self.books.append(new_book)
            print(f"{Fore.GREEN}✓ Book '{new_book.title}' added successfully.{Style.RESET_ALL}")
            self.save_data() # Save immediately after adding
            return True
        except ValueError as e:
            print(f"{Fore.RED}✗ Failed to add book: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}✗ An unexpected error occurred while adding book: {e}{Style.RESET_ALL}")
            return False

    def view_all_books(self):
        """Displays details of all books in the inventory."""
        if not self.books:
            print(f"{Fore.YELLOW}No books in the inventory yet.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}═══ Current Inventory ═══{Style.RESET_ALL}")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")
        print(f"{Fore.CYAN}═════════════════════════{Style.RESET_ALL}")

    def find_books(self, search_term):
    
        search_term_lower = search_term.strip().lower()
        found_books = [
            book for book in self.books 
            if search_term_lower in book.title.lower() or search_term_lower in book.author.lower()
        ]
        return found_books

    def update_book(self, book_to_update, new_title=None, new_author=None, new_price=None, new_stock=None):
   
        updated = False
        try:
            if new_title is not None and new_title.strip():
                # Prevent changing title to an existing one (title+author unique)
                # Ensure we don't compare against itself when checking for duplicates
                if new_title.lower() != book_to_update.title.lower() and \
                   any(b.title.lower() == new_title.lower() and b.author.lower() == book_to_update.author.lower() 
                       for b in self.books if b is not book_to_update): # Use 'is not' for object identity
                    print(f"{Fore.RED}✗ A book with title '{new_title}' by {book_to_update.author} already exists. Title not updated.{Style.RESET_ALL}")
                else:
                    book_to_update.title = Book._validate_string_input(new_title, "Title")
                    updated = True
            
            if new_author is not None and new_author.strip():
                # Prevent changing author to an existing one (title+author unique)
                if new_author.lower() != book_to_update.author.lower() and \
                   any(b.title.lower() == book_to_update.title.lower() and b.author.lower() == new_author.lower()
                       for b in self.books if b is not book_to_update): # Use 'is not' for object identity
                    print(f"{Fore.RED}✗ A book with title '{book_to_update.title}' by '{new_author}' already exists. Author not updated.{Style.RESET_ALL}")
                else:
                    book_to_update.author = Book._validate_string_input(new_author, "Author")
                    updated = True
            
            if new_price is not None:
                book_to_update.price = Book._validate_price(new_price)
                updated = True
            
            if new_stock is not None:
                book_to_update.stock = Book._validate_stock(new_stock)
                updated = True
            
            if updated:
                self.save_data()
                print(f"{Fore.GREEN}✓ Book '{book_to_update.title}' updated successfully.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}No changes applied to '{book_to_update.title}'.{Style.RESET_ALL}")
            return updated
        except ValueError as e:
            print(f"{Fore.RED}✗ Error updating book: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}✗ An unexpected error occurred while updating book: {e}{Style.RESET_ALL}")
            return False

    def delete_book(self, book_to_delete):
      
        if book_to_delete in self.books:
            self.books.remove(book_to_delete)
            self.save_data()
            print(f"{Fore.GREEN}✓ Book '{book_to_delete.title}' by {book_to_delete.author} deleted successfully.{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}✗ Book not found in inventory. Deletion failed.{Style.RESET_ALL}")
            return False

    def adjust_stock(self, book_to_adjust, quantity_change):
       
        try:
            new_stock = book_to_adjust.stock + quantity_change
            book_to_adjust.stock = Book._validate_stock(new_stock) # Re-use validation for non-negative
            self.save_data()
            print(f"{Fore.GREEN}✓ Stock for '{book_to_adjust.title}' adjusted. New stock: {book_to_adjust.stock}{Style.RESET_ALL}")
            return True
        except ValueError as e:
            print(f"{Fore.RED}✗ Failed to adjust stock: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}✗ An unexpected error occurred while adjusting stock: {e}{Style.RESET_ALL}")
            return False

    def save_data(self):
        """Wrapper to save all books to file."""
        return save_books_to_file(self.books)

    def load_data(self):
        """Wrapper to load all books from file."""
        self.books = load_books_from_file()
        # load_books_from_file already handles errors and returns [], so no need for 'is not None'
        return True