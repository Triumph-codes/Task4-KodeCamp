# student_manager.py

import json
import os
from pathlib import Path
from apps.student_app.student import Student # Import the Student class
from colorama import Fore, Style # For print statements
from shared.utils import get_valid_input, confirm_action # Import shared utilities


DATA_FILE = 'students.json' 

def save_students_to_file(students_list):
    """Save a list of Student objects to JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump([s.to_dict() for s in students_list], f, indent=4)
        print(f"{Fore.GREEN}✓ Student data saved successfully to '{DATA_FILE}'{Style.RESET_ALL}")
        return True
    except IOError as e:
        print(f"{Fore.RED}✗ Error saving student data: {e}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}✗ An unexpected error occurred while saving: {e}{Style.RESET_ALL}")
        return False

def load_students_from_file():
    """Load a list of Student objects from JSON file."""
    if not Path(DATA_FILE).exists():
        print(f"{Fore.YELLOW}⚠ No student data file '{DATA_FILE}' found. Starting with an empty list.{Style.RESET_ALL}")
        return []
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        
        # Convert dictionaries back into Student objects
        students = [Student.from_dict(s_data) for s_data in data]
        print(f"{Fore.GREEN}✓ Loaded {len(students)} students from '{DATA_FILE}'{Style.RESET_ALL}")
        return students
    except json.JSONDecodeError:
        print(f"{Fore.RED}✗ Student data file '{DATA_FILE}' is corrupted. Starting with an empty list.{Style.RESET_ALL}")
        return []
    except IOError as e:
        print(f"{Fore.RED}✗ Error loading student data: {e}{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED}✗ An unexpected error occurred while loading: {e}{Style.RESET_ALL}")
        return []

class StudentManager:
    def __init__(self):
        self.students = []
        self._load_initial_data()

    def _load_initial_data(self):
        """Loads student data when the manager is initialized."""
        self.students = load_students_from_file()

    def add_student(self, name, subjects_scores):
        """Add a new student to the manager."""
        try:
            new_student = Student(name, subjects_scores)
            # Check for duplicate student name (assuming names should be unique for simplicity)
            if any(s.name.lower() == new_student.name.lower() for s in self.students):
                print(f"{Fore.RED}✗ Failed to add student: Student with name '{new_student.name}' already exists.{Style.RESET_ALL}")
                return False
            
            self.students.append(new_student)
            print(f"{Fore.GREEN}✓ Student '{new_student.name}' added successfully.{Style.RESET_ALL}")
            self.save_data() # Save immediately after adding
            return True
        except ValueError as e:
            print(f"{Fore.RED}✗ Failed to add student: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}✗ An unexpected error occurred while adding student: {e}{Style.RESET_ALL}")
            return False

    def view_all_students(self):
        """Display details of all students."""
        if not self.students:
            print(f"{Fore.YELLOW}No students in the records yet.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}═══ All Student Records ═══{Style.RESET_ALL}")
        for i, student in enumerate(self.students, 1):
            print(f"{i}. {student}")
        print(f"{Fore.CYAN}═══════════════════════════{Style.RESET_ALL}")

    def find_student_by_name(self, name):
        """Find a student by name (case-insensitive, partial match)."""
        name_lower = name.strip().lower()
        found_students = [s for s in self.students if name_lower in s.name.lower()]
        return found_students
    
    def update_student(self, search_name):
        """Update an existing student's details."""
        found_students = self.find_student_by_name(search_name)

        if not found_students:
            print(f"{Fore.YELLOW}No student found matching '{search_name}'.{Style.RESET_ALL}")
            return False
        
        student_to_update = None
        if len(found_students) == 1:
            student_to_update = found_students[0]
        else:
            print(f"{Fore.YELLOW}Multiple students found:{Style.RESET_ALL}")
            for i, s in enumerate(found_students, 1):
                print(f"{i}. {s.name}")
            
            choice_index = get_valid_input("Enter the number of the student to update: ", int, 
                                           lambda x: 1 <= x <= len(found_students), 
                                           "Invalid number.")
            student_to_update = found_students[choice_index - 1]

        print(f"\n{Fore.CYAN}Updating student: {student_to_update.name}{Style.RESET_ALL}")
        
        new_name = input(f"Enter new name (current: {student_to_update.name}, leave blank to keep): ").strip()
        if new_name:
            # Check for duplicate name if changed
            if new_name.lower() != student_to_update.name.lower() and \
               any(s.name.lower() == new_name.lower() for s in self.students if s != student_to_update):
                print(f"{Fore.RED}✗ A student with name '{new_name}' already exists. Name not updated.{Style.RESET_ALL}")
            else:
                student_to_update.name = new_name
                print(f"{Fore.GREEN}Name updated to '{new_name}'.{Style.RESET_ALL}")
        
        # Option to update subjects/scores (this could be more elaborate)
        update_scores_choice = input("Do you want to update subjects/scores? (yes/no): ").lower().strip()
        if update_scores_choice == 'yes':
            print("Enter new scores (e.g., Math:90,Science:85). Leave blank to keep existing scores for a subject.")
            print(f"Current scores: {student_to_update.subjects_scores}")
            new_scores_str = input("Enter new scores: ").strip()
            if new_scores_str:
                updated_scores = student_to_update.subjects_scores.copy() # Start with current scores
                try:
                    for item in new_scores_str.split(','):
                        subject, score_str = item.split(':')
                        updated_scores[subject.strip()] = int(score_str.strip())
                    student_to_update.subjects_scores = updated_scores
                    print(f"{Fore.GREEN}Subjects/scores updated.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}✗ Invalid score format. Please use 'Subject:Score,Subject:Score'. Scores not updated.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}✗ An error occurred while updating scores: {e}. Scores not updated.{Style.RESET_ALL}")

        self.save_data() # Save changes after update
        print(f"{Fore.GREEN}✓ Student '{student_to_update.name}' updated successfully.{Style.RESET_ALL}")
        return True

    def delete_student(self, search_name):
        """Delete a student by name."""
        found_students = self.find_student_by_name(search_name)

        if not found_students:
            print(f"{Fore.YELLOW}No student found matching '{search_name}'.{Style.RESET_ALL}")
            return False
        
        student_to_delete = None
        if len(found_students) == 1:
            student_to_delete = found_students[0]
        else:
            print(f"{Fore.YELLOW}Multiple students found:{Style.RESET_ALL}")
            for i, s in enumerate(found_students, 1):
                print(f"{i}. {s.name}")
            
            choice_index = get_valid_input("Enter the number of the student to delete: ", int, 
                                           lambda x: 1 <= x <= len(found_students), 
                                           "Invalid number.")
            student_to_delete = found_students[choice_index - 1]

        if confirm_action(f"Are you sure you want to delete student '{student_to_delete.name}'?"):
            self.students = [s for s in self.students if s != student_to_delete] # Use object comparison for exact match
            self.save_data() # Save immediately after deleting
            print(f"{Fore.GREEN}✓ Student '{student_to_delete.name}' deleted successfully.{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}Deletion of '{student_to_delete.name}' cancelled.{Style.RESET_ALL}")
            return False

    def save_data(self):
        """Wrapper to save all students to file."""
        return save_students_to_file(self.students)

    def load_data(self):
        """Wrapper to load all students from file."""
        self.students = load_students_from_file()
        return True 