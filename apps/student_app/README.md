# Student Report Card App

This is a terminal-based application built with Python to manage student scores and grades. It's part of a larger project suite but can also be understood as a standalone component.

## Features:
-   **Student Class:** Manages student data including name, subjects, individual scores, calculated average score, and assigned letter grade.
-   **Add New Students:** Allows interactive input for student names and multiple subject scores.
-   **View All Students:** Displays a comprehensive list of all recorded students with their details, average scores, and grades.
-   **Search Students:** Enables searching for students by name (supports partial and case-insensitive matching).
-   **Data Persistence:** Saves and loads all student records to/from a `students.json` file, ensuring data is retained across sessions.
-   **Robust Input Validation:** Ensures all user inputs (names, subjects, scores) adhere to predefined rules and formats, providing clear error messages.
-   **Colored Output:** Utilizes `colorama` for enhanced readability and user experience in the terminal.

## How to Run:
This application is designed to be run via the main unified menu system from the project root.
1.  Navigate to the root directory of the entire project.
2.  Run `python main.py`.
3.  Select the "Student Report Card App" option from the main menu.

Alternatively, for standalone testing (not recommended for daily use in the unified project):
1.  Navigate into the `student_app/` directory.
2.  Run `python main.py`.