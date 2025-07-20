# inventory.py

import json
import os
import math
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

    def save_data(self):
        """Wrapper to save all books to file."""
        return save_books_to_file(self.books)

    def load_data(self):
        """Wrapper to load all books from file."""
        loaded_books = load_books_from_file()
        if loaded_books is not None: # load_books_from_file returns [] on error/no file
            self.books = loaded_books
            return True
        return False