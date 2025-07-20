# student.py

from colorama import Fore, Style # Only for __str__ method's display
print(f"{Fore.GREEN}DEBUG: student_app/student.py loaded. __name__='{__name__}', __package__='{__package__}'{Style.RESET_ALL}")


class Student:
    VALID_GRADES = {
        'A': (90, 100),
        'B': (80, 89),
        'C': (70, 79),
        'D': (60, 69),
        'F': (0, 59)
    }
    VALID_SUBJECTS = ['Math', 'Science', 'English', 'History', 'Art', 'Music', 'PE', 'Computer Science'] # Example subjects

    def __init__(self, name, subjects_scores):
        self.name = self._validate_name(name)
        self.subjects_scores = self._validate_subjects_scores(subjects_scores)
        self._average = self._calculate_average() # Private attribute, calculated on init
        self._grade = self._assign_grade()       # Private attribute, calculated on init

    @staticmethod
    def _validate_name(name):
        """Validate student name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Student name cannot be empty.")
        name = name.strip()
        if len(name) < 2 or len(name) > 100:
            raise ValueError("Name must be between 2 and 100 characters.")
        if not all(c.isalpha() or c.isspace() or c in "-'." for c in name):
            raise ValueError("Name contains invalid characters (only letters, spaces, hyphens, apostrophes, periods allowed).")
        return ' '.join(word.capitalize() for word in name.split())

    @staticmethod
    def _validate_subject_name(subject):
        """Validate a single subject name."""
        if not isinstance(subject, str) or not subject.strip():
            raise ValueError("Subject name cannot be empty.")
        subject = subject.strip().title() # Capitalize for consistency
        if subject not in Student.VALID_SUBJECTS:
            raise ValueError(f"Invalid subject: '{subject}'. Choose from: {', '.join(Student.VALID_SUBJECTS)}.")
        return subject

    @staticmethod
    def _validate_score(score):
        """Validate a single score."""
        try:
            score = float(score)
        except (ValueError, TypeError):
            raise ValueError("Score must be a number.")
        if not (0 <= score <= 100):
            raise ValueError("Score must be between 0 and 100.")
        return round(score, 2) # Store scores with 2 decimal places

    def _validate_subjects_scores(self, subjects_scores):
        """Validate the dictionary of subjects and scores."""
        if not isinstance(subjects_scores, dict) or not subjects_scores:
            raise ValueError("Subjects and scores must be a non-empty dictionary.")
        
        validated_data = {}
        for subject, score in subjects_scores.items():
            valid_subject = self._validate_subject_name(subject)
            valid_score = self._validate_score(score)
            validated_data[valid_subject] = valid_score
        return validated_data

    def _calculate_average(self):
        """Calculate the average score."""
        if not self.subjects_scores:
            return 0.0
        total_score = sum(self.subjects_scores.values())
        return round(total_score / len(self.subjects_scores), 2)

    def _assign_grade(self):
        """Assign a letter grade based on the average score."""
        avg = self._average
        for grade, (min_score, max_score) in self.VALID_GRADES.items():
            if min_score <= avg <= max_score:
                return grade
        return 'N/A' # Should not happen if grades cover 0-100

    @property
    def average(self):
        """Public getter for average, recalculates if scores change."""
        return self._calculate_average()

    @property
    def grade(self):
        """Public getter for grade, recalculates if average changes."""
        return self._assign_grade()

    def __str__(self):
        subject_lines = "\n".join([
            f"    - {Fore.BLUE}{sub}{Style.RESET_ALL}: {Fore.MAGENTA}{score:.2f}{Style.RESET_ALL}"
            for sub, score in self.subjects_scores.items()
        ])
        return (
            f"\n{Fore.CYAN}Student: {self.name}{Style.RESET_ALL}\n"
            f"  {Fore.GREEN}Average Score:{Style.RESET_ALL} {self.average:.2f}\n"
            f"  {Fore.GREEN}Grade:{Style.RESET_ALL} {self.grade}\n"
            f"  {Fore.YELLOW}Subjects & Scores:{Style.RESET_ALL}\n{subject_lines}"
        )

    def to_dict(self):
        """Convert Student object to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'subjects_scores': self.subjects_scores,
            # Average and Grade are derived, so no need to store them directly
        }

    @classmethod
    def from_dict(cls, data):
        """Create Student object from dictionary."""
        return cls(data['name'], data['subjects_scores'])