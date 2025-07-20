
import os
import sys
from colorama import init, Fore, Style 
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from apps.student_app.main import run_student_app
    from apps.bookstore_app.main import run_bookstore_app
    from apps.budget_app.main import run_budget_app
    from shared.utils import get_valid_input
except ImportError as e:
    print(f"{Fore.RED}Critical Error: {e}{Style.RESET_ALL}")
    sys.exit(1)


def display_main_menu():
    """Displays the main application selection menu."""
    print(f"\n{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}          LMS Python Project V.4 🚀          {Style.RESET_ALL}")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.BLUE}1.{Style.RESET_ALL} Student Report Card App")
    print(f"{Fore.BLUE}2.{Style.RESET_ALL} Bookstore Inventory System")
    print(f"{Fore.BLUE}3.{Style.RESET_ALL} Personal Budget Tracker")
    print(f"{Fore.BLUE}4.{Style.RESET_ALL} Exit Unified Application")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")

def main():
    """Main function to run the unified application suite."""
    while True:
        display_main_menu()

        choice = get_valid_input("Enter your choice (1-4):",
                                 validator=lambda x: x if x in ['1','2','3','4']
                                 else (_ for _ in ()).throw(ValueError("Invalid choice. Please enter a number between 1 and 4.")))

        if choice is None:
            continue

        if choice == '1':
            run_student_app()
        elif choice == '2':
            run_bookstore_app()
        elif choice == '3':
            run_budget_app()
        elif choice == '4':
            print(f"{Fore.GREEN}Exiting the unified application. Goodbye! 👋{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()

