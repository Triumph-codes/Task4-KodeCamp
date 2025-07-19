# Bookstore Inventory System

This is a terminal-based application built with Python to manage the inventory of books in a bookstore. It's part of a larger project suite but can also be understood as a standalone component.

## Features:
-   **Book Class:** Manages book details including title, author, price, and current stock quantity.
-   **Add New Books:** Allows interactive input for new book details and automatically handles adding them to the inventory.
-   **View All Books:** Displays a comprehensive list of all books currently in stock.
-   **Data Persistence:** Saves and loads all inventory data to/from a `books.json` file, ensuring stock levels are retained across sessions.
-   **Price Rounding:** Uses the `math` module to ensure prices are correctly rounded for financial accuracy.
-   **Robust Input Validation:** Ensures all user inputs (title, author, price, stock) adhere to predefined rules and formats, providing clear error messages.
-   **Colored Output:** Utilizes `colorama` for enhanced readability and user experience in the terminal.
-   **Future Feature (Search):** Designed with a placeholder for upcoming search functionality by title or author.

## How to Run:
This application is designed to be run via the main unified menu system from the project root.
1.  Navigate to the root directory of the entire project.
2.  Run `python main.py`.
3.  Select the "Bookstore Inventory System" option from the main menu.

Alternatively, for standalone testing (not recommended for daily use in the unified project):
1.  Navigate into the `bookstore_app/` directory.
2.  Run `python main.py`.