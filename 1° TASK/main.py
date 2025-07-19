# main.py

from utils import setup_app_colors, get_valid_input
from student import Student # To access VALID_SUBJECTS and static validation methods
from student_manager import StudentManager
from colorama import Fore, Style # For direct print statements in main

def display_main_menu():
    """Displays the main menu options."""
    print(f"\n{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}          Student Report Card App 🎓          {Style.RESET_ALL}")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.BLUE}1.{Style.RESET_ALL} Add New Student")
    print(f"{Fore.BLUE}2.{Style.RESET_ALL} View All Students")
    print(f"{Fore.BLUE}3.{Style.RESET_ALL} Search Student by Name")
    # Update/Delete features will be added in future commits
    print(f"{Fore.BLUE}4.{Style.RESET_ALL} Save Student Data")
    print(f"{Fore.BLUE}5.{Style.RESET_ALL} Load Student Data")
    print(f"{Fore.BLUE}6.{Style.RESET_ALL} Exit Application")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════════════{Style.RESET_ALL}")

def get_student_subjects_scores():
    """Interactively gets subjects and scores for a new student."""
    subjects_scores = {}
    print(f"\n{Fore.CYAN}--- Enter Subject Scores (type 'done' to finish) ---{Style.RESET_ALL}")
    while True:
        subject_name_input = get_valid_input(
            f"Enter subject name (e.g., Math, Science, or 'done'):{Style.RESET_ALL} ",
            validator=lambda x: x.strip().title() if x.strip().lower() != 'done' else 'done'
        )
        if subject_name_input is None: # User cancelled
            return None
        if subject_name_input.lower() == 'done':
            break

        try:
            # Validate subject name against predefined list
            validated_subject = Student._validate_subject_name(subject_name_input)
            if validated_subject in subjects_scores:
                print(f"{Fore.YELLOW}Warning: Score for '{validated_subject}' already entered. It will be overwritten.{Style.RESET_ALL}")
            
            score_input = get_valid_input(
                f"Enter score for {validated_subject} (0-100):{Style.RESET_ALL} ",
                validator=Student._validate_score
            )
            if score_input is None: # User cancelled score input for this subject
                print(f"{Fore.YELLOW}Score input cancelled for {validated_subject}. This subject will not be added.{Style.RESET_ALL}")
                continue # Allow user to enter another subject or 'done'
            
            subjects_scores[validated_subject] = score_input
            print(f"{Fore.GREEN}✓ Added score for {validated_subject}.{Style.RESET_ALL}")

        except ValueError as e:
            print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
            # get_valid_input handles max_attempts, so this catch is for Student._validate_subject_name
            # which is called directly here.
            continue # Allow re-entry for subject/score

    if not subjects_scores:
        print(f"{Fore.RED}✗ No subjects and scores entered. Student cannot be added without scores.{Style.RESET_ALL}")
        return None
    return subjects_scores


def main():
    setup_app_colors() # Initialize colorama
    manager = StudentManager() # Automatically loads data on init

    while True:
        display_main_menu()
        
        choice = get_valid_input("Enter your choice (1-6):", 
                                 validator=lambda x: x if x in ['1','2','3','4','5','6'] 
                                 else (_ for _ in ()).throw(ValueError("Invalid choice. Please enter a number between 1 and 6.")))
        
        if choice is None: # User cancelled menu input
            continue 

        if choice == '1': # Add New Student
            print(f"\n{Fore.CYAN}═══ Add New Student ═══{Style.RESET_ALL}")
            name = get_valid_input("Enter student's full name:", validator=Student._validate_name)
            if name is None: continue

            subjects_scores = get_student_subjects_scores()
            if subjects_scores is None: continue # User cancelled or no scores entered

            manager.add_student(name, subjects_scores)
        
        elif choice == '2': # View All Students
            manager.view_all_students()
        
        elif choice == '3': # Search Student by Name
            print(f"\n{Fore.CYAN}═══ Search Student ═══{Style.RESET_ALL}")
            search_name = get_valid_input("Enter student name to search (partial match allowed):", validator=Student._validate_name)
            if search_name is None: continue
            
            found_students = manager.find_student_by_name(search_name)
            if found_students:
                print(f"\n{Fore.GREEN}Found {len(found_students)} matching student(s):{Style.RESET_ALL}")
                for i, student in enumerate(found_students, 1):
                    print(f"{i}. {student.name} (Avg: {student.average:.2f}, Grade: {student.grade})")
            else:
                print(f"{Fore.YELLOW}No students found matching '{search_name}'.{Style.RESET_ALL}")

        elif choice == '4': # Save Student Data
            manager.save_data()
        
        elif choice == '5': # Load Student Data
            # Ask for confirmation before overwriting in-memory data
            if manager.students: # Only ask if there's data in memory
                confirm = get_valid_input(
                    f"{Fore.YELLOW}Warning: Loading new data will overwrite current unsaved changes. Proceed? (yes/no):{Style.RESET_ALL} ",
                    validator=lambda x: x.lower() if x.lower() in ['yes', 'no'] else (_ for _ in ()).throw(ValueError("Invalid input. Please enter 'yes' or 'no'.")))
                if confirm != 'yes':
                    print(f"{Fore.BLUE}Loading cancelled.{Style.RESET_ALL}")
                    continue
            
            manager.load_data() # This will reassign manager.students internally
        
        elif choice == '6': # Exit Application
            confirm_exit = get_valid_input(
                f"{Fore.YELLOW}Exit without saving current changes? (yes/no):{Style.RESET_ALL} ",
                validator=lambda x: x.lower() if x.lower() in ['yes', 'no'] else (_ for _ in ()).throw(ValueError("Invalid input. Please enter 'yes' or 'no'.")))
            if confirm_exit == 'yes':
                print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                break
            elif confirm_exit is None: # User cancelled exit, stay in app
                print(f"{Fore.BLUE}Exit cancelled.{Style.RESET_ALL}")
                continue
            else:
                print(f"{Fore.BLUE}Exit cancelled. Returning to main menu.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()