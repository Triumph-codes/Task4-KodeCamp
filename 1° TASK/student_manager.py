# student_manager.py

import json
import os
from pathlib import Path
from student import Student # Import the Student class
from colorama import Fore, Style # For print statements

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
                raise ValueError(f"Student with name '{new_student.name}' already exists.")
            
            self.students.append(new_student)
            print(f"{Fore.GREEN}✓ Student '{new_student.name}' added successfully.{Style.RESET_ALL}")
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

    def save_data(self):
        """Wrapper to save all students to file."""
        return save_students_to_file(self.students)

    def load_data(self):
        """Wrapper to load all students from file."""
        loaded_students = load_students_from_file()
        if loaded_students is not None: # load_students_from_file returns [] on error/no file
            self.students = loaded_students
            return True
        return False