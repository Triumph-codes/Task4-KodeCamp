# Personal Budget Tracker

This is a terminal-based application built with Python to help you track and categorize your personal expenses and income.

## Features:
- Add new transactions (date, category, amount)
- View all recorded transactions
- Group and view transactions by category with their respective totals
- Calculate overall total expenses and net balance
- Save and load transaction data to/from a JSON file for persistence
- Robust input validation for all entries
- Colored output for better readability in the terminal

## How to Run:
1.  **Prerequisites:** Make sure you have Python 3 installed.
2.  **Install Dependencies:**
    This project uses `colorama` for colored terminal output. Install it using pip:
    ```bash
    pip install colorama
    ```
3.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
    cd your-repo-name
    ```
    (Note: Replace `yourusername/your-repo-name.git` with your actual repository URL after you push it to GitHub.)
4.  **Run the Application:**
    ```bash
    python main.py
    ```

## Project Structure:
- `main.py`: The main entry point of the application, handling the user interface and menu.
- `transaction.py`: Defines the `Transaction` class, which represents individual financial entries.
- `budget_tracker.py`: Contains the `BudgetTracker` class, responsible for managing a collection of transactions and performing calculations.
- `utils.py`: Provides utility functions like `get_valid_input` for robust user input handling and `setup_app_colors` for terminal styling.
- `transactions.json`: (Created automatically) Stores your transaction data persistently.

## Usage:
Follow the on-screen menu to add transactions, view summaries, and manage your budget.