# Task4-KodeCamp
Fourth promotional task on KodeCamp
comprising of :
Task 1: Student Report Card App (with Version History)
Task 2: Bookstore Inventory System (Using Git Branches)
Task 3: Personal Budget Tracker



This repository contains a collection of independent Python terminal applications developed as part of an LMS challenge. Each task is a separate application, currently designed to be run individually from its own directory.

📂 Project Structure:
This project is structured with individual folders for each task. Here's a typical layout (note: folder names might vary slightly on your system, e.g., 2° TASK for the Bookstore App):
'''
ProjectRoot/
├── README.md               # This file
├── utils.py                # Common utility functions (e.g., input validation, colors)
|
├── Task1_StudentApp/       # Directory for Task 1: Student Report Card App
│   ├── main.py             # Main script for the Student App
│   ├── student.py
│   └── student_manager.py
|
├── Task2_BookstoreApp/     # Directory for Task 2: Bookstore Inventory System
│   ├── main.py             # Main script for the Bookstore App
│   ├── book.py
│   └── inventory.py
|
└── Task3_BudgetApp/        # Directory for Task 3: Personal Budget Tracker
    ├── main.py             # Main script for the Budget App
    ├── transaction.py
    └── budget_tracker.py
'''
🚀 How to Run Each Application:
Since these applications are currently standalone, you'll need to navigate into their respective directories to run them.

Prerequisites: Make sure you have Python 3 installed on your system.

Install Dependencies: This project uses the colorama library for enhanced terminal output. Install it using pip:

Bash

pip install colorama
Clone the Repository: If you haven't already, clone this repository to your local machine:



📚 Task Details:
Task 1: Student Report Card App
Goal: To effectively manage student academic records, including scores and grades.

Key Files: main.py, student.py, student_manager.py (located in its task directory).

Features:

Student Class: Defines student entities with attributes like name, subjects, individual scores, calculated average score, and an assigned letter grade.

Adding New Students: Provides an interactive interface to add student names and multiple subject scores.

Viewing All Students: Displays a comprehensive list of all recorded students with their details, average scores, and grades.

Searching Students: Enables searching for students by name (supports partial and case-insensitive matching).

Data Persistence: Student data is securely saved to and loaded from a students.json file, ensuring data is retained across application sessions.

Robust Input Validation: Incorporates strict validation for all user inputs (names, subjects, scores) to prevent errors and ensure data quality, with helpful error messages.

Colored Output: Utilizes colorama for enhanced readability and user experience in the terminal.

Task 2: Bookstore Inventory System
Goal: To manage and track the inventory of books within a bookstore.

Key Files: main.py, book.py, inventory.py (located in its task directory).

Features:

Book Class: Defines book entities, detailing properties such as title, author, price, and current stock quantity.

Adding New Books: Offers an interactive way to add new books to the inventory, capturing all necessary details.

Viewing All Books: Presents a comprehensive list of all books currently in stock.

Data Persistence: Inventory data is saved to and loaded from a books.json file, ensuring stock levels are maintained between application runs.

Price Rounding: Uses the math module to ensure that all book prices are accurately rounded for financial accuracy.

Robust Input Validation: Implements thorough validation for all user inputs (title, author, price, stock) to maintain data consistency and prevent invalid entries.

Colored Output: Improves terminal readability and user experience with clear, colored text.

Future Feature (Search): Designed with a placeholder for upcoming search functionality, allowing users to find books by title or author.

Task 3: Personal Budget Tracker
Goal: To help users track, categorize, and analyze their personal expenses and income.

Key Files: main.py, transaction.py, budget_tracker.py (located in its task directory).

Features:

Transaction Class: Defines individual financial transactions, including date, category, and amount.

Adding New Transactions: Allows users to easily add new financial transactions with validated details.

Viewing All Transactions: Displays a detailed list of all recorded transactions.

Categorized Views: Enables grouping and viewing transactions by specific categories, along with their respective subtotals.

Expense Calculation: Provides functionality to calculate overall total expenses and derive a net balance.

Data Persistence: Transaction data is saved to and loaded from a transactions.json file, ensuring all financial records are securely stored.

Robust Input Validation: Ensures all entries (date, category, amount) are valid and correctly formatted, with clear error feedback.

Colored Output: Utilizes colorama for better readability and a more engaging terminal experience.

🔧 Common Utilities:
utils.py: This essential file, located in the project root, provides shared utility functions that are utilized across all applications. Key utilities include get_valid_input for consistent and robust user input handling, and setup_app_colors for initializing and managing terminal styling, ensuring a cohesive look and feel throughout the suite.