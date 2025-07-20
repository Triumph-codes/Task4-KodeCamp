# shared/utils.py

from colorama import Fore, Style, init
import sys
import os # This import is not strictly used in this snippet, but harmless.

def setup_app_colors():
    """Initializes colorama for colored terminal output."""
    init(autoreset=True)


def get_valid_input(prompt, validator=None, type_func=str, allow_empty=False,
                    error_message="Invalid input. Please try again.", max_attempts=0):

    attempts = 0
    while True: # Main loop runs indefinitely until valid input, cancellation, or max attempts
        if max_attempts > 0 and attempts >= max_attempts:
            print(f"{Fore.RED}Maximum input attempts ({max_attempts}) exceeded. Operation cancelled.{Style.RESET_ALL}")
            return None

        try:
            # Use 'c' for cancel, more common than 'cancel' for brevity
            user_input = input(f"{Fore.LIGHTCYAN_EX}{prompt}{Style.RESET_ALL} (or 'c' to cancel): ").strip()

            if user_input.lower() == 'c':
                print(f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
                return None

            if allow_empty and not user_input:
                return "" # Return empty string if allowed and input is empty, skipping further validation/conversion

            # --- Core Logic for Type Conversion and Validation ---
            converted_input = type_func(user_input) # First, attempt type conversion

            if validator:
                # Then, validate the converted input
                validated_input = validator(converted_input)
                return validated_input # If validator passes, return the validated input
            else:
                return converted_input # If no validator, return the converted input directly

        except ValueError as e:
            attempts += 1
            # Print the specific error message from the parameter, plus the original ValueError message
            print(f"{Fore.RED}✗ Error: {error_message} ({e}){Style.RESET_ALL}")
            if max_attempts > 0: # Only show attempts remaining if max_attempts is enabled
                print(f"{Fore.YELLOW}Attempts remaining:{Style.RESET_ALL} {max_attempts-attempts}")
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print(f"\n{Fore.YELLOW}Operation cancelled by user (Ctrl+C).{Style.RESET_ALL}")
            return None # Indicate cancellation
        except Exception as e: # Catch any other unexpected errors during input
            attempts += 1
            print(f"{Fore.RED}✗ An unexpected error occurred during input: {e}{Style.RESET_ALL}")
            if max_attempts > 0:
                print(f"{Fore.YELLOW}Attempts remaining:{Style.RESET_ALL} {max_attempts-attempts}")

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