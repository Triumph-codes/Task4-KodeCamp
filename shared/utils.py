# utils.py

from colorama import Fore, Style, init
import sys

def setup_app_colors():
    """Initializes colorama for colored terminal output."""
    init(autoreset=True)

def get_valid_input(prompt, validator=None, max_attempts=3):
    """
    Gets validated user input with multiple attempts.
    Prints error messages in red. Allows 'cancel' or Ctrl+C to abort.
    """
    attempts = 0
    while attempts < max_attempts:
        try:
            value = input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL} ").strip()
            
            # Allow cancellation by typing 'cancel' or pressing Ctrl+C
            if value.lower() == 'cancel':
                print(f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
                return None
            
            if validator:
                return validator(value)
            return value
        except ValueError as e:
            attempts += 1
            print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
            if attempts == max_attempts:
                print(f"{Fore.RED}Maximum attempts reached. Returning to previous menu.{Style.RESET_ALL}")
                return None
            print(f"{Fore.YELLOW}Attempts remaining:{Style.RESET_ALL} {max_attempts-attempts}")
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print(f"\n{Fore.YELLOW}Operation cancelled by user (Ctrl+C).{Style.RESET_ALL}")
            return None # Indicate cancellation

def confirm_action(prompt):
    """Asks the user for confirmation (yes/no)."""
    while True:
        response = input(f"{Fore.YELLOW}{prompt} (yes/no): {Style.RESET_ALL}").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print(f"{Fore.RED}Invalid input. Please type 'yes' or 'no'.{Style.RESET_ALL}")