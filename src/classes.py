"""
classes.py

This file contains:
1) Subject:   holds subject id + mark + grade
2) Student:   holds profile + a list of Subject + overall average + pass/fail
3) Database:  reads/writes students to 'students.data' and exposes actions
              (add student, enrol, remove subject, list/group/partition, etc.)

Design notes:
- I store all students as a JSON in 'students.data' (Text)
- I recompute 'overall' and 'status' every time subjects change.
- A student can enrol in at most 4 subjects (enforced in Database.enrol()).
- When program start load data from student.data to memory. After any changes, save everything back to the same file

Nicha: Done Final ver.
"""

import json
import random

import check_func
# Validation functions:
# - get_grade(mark): returns Z/P/C/D/HD
# - check_email(), check_password():
# - generate_student_id(), generate_subject_id()


# ---------------------------------------------------------------------
# 1) Subject Class

class Subject:
    def __init__(self, subject_id: str, mark: int):
        self.id = f"{int(subject_id):03d}"  # store as 3-digit string, e.g. "001"
        self.mark = int(mark)
        self.grade = check_func.get_grade(self.mark)

    @staticmethod
    def from_dict(data: dict) -> "Subject":
        return Subject(data["id"], data["mark"])
    
    def to_dict(self) -> dict:
        return {"id": self.id, "mark": self.mark, "grade": self.grade}
    
# ---------------------------------------------------------------------
# 2) Student Class

class Student:
    """
    A student has:
      - email, name, password
      - id: 6-digit string (e.g., "000123")
      - subjects: list[Subject]
      - overall: average of all subject marks (float, 0 if empty)
      - status: True = PASS (overall >= 50), False = FAIL
      - overall recal everytime subject change
      - status recal when overall change
    """
    def __init__(self, email: str, password: str, name: str,
                 subjects: list, student_id: str, overall: float, status: bool):
        self.email = email
        self.password = password
        self.name = name
        self.subjects: list[Subject] = subjects
        self.id = f"{int(student_id):06d}"       # store as 6-digit string, e.g. "000123"
        self.overall = float(overall)
        self.status = bool(status)

    @staticmethod
    def from_dict(data: dict) -> "Student":
        """Rebuild a Student from its dict (including nested Subject dicts)."""
        subjects = [Subject.from_dict(s) for s in data.get("subjects", [])]
        return Student(
            email=data["email"],
            password=data["password"],
            name=data["name"],
            subjects=subjects,
            student_id=data["id"],
            overall=data.get("overall", 0),
            status=data.get("status", False),
        )

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "subjects": [s.to_dict() for s in self.subjects],
            "id": self.id,
            "overall": self.overall,
            "status": self.status,
        }

    # Create method to keep overall + status consistent
    def _recompute_overall_and_status(self) -> None:
        """Recalculate overall average and pass/fail status."""
        if len(self.subjects) == 0:
            self.overall = 0.0
            self.status = False
            return

        total = sum(s.mark for s in self.subjects)
        self.overall = round(total / len(self.subjects), 2)
        self.status = (self.overall >= 50)   # average >= 50 is PASS


# ---------------------------------------------------------------------
# 3) Database
# ---------------------------------------------------------------------
class Database:
    """
    This class owns the list of students in memory and takes care of reading/writing
    to the 'students.data' file.

    List methods that the CLI/GUI can call:
      - add_student(email, password, name)
      - enrol(student_id)
      - remove_subject(student_id, subject_id)
      - change_password(student_id, new_password)
      - show_students (options)       # 1=list, 2=group-by-grade, 3=pass/fail
      - remove_student(student_id)
      - remove_all()
      - check_db_email
    """
    FILE_NAME = "students.data"

    def __init__(self):
        self.students: list[Student] = self.load_students()

    # -----------------------------
    # load & save data JSON <> Dictionary <> Object
    # -----------------------------
    def load_students(self) -> list:
        """
        Read the JSON file. If not found, return an empty list.
        Store students as a JSON list
        """
        try:
            with open(self.FILE_NAME, "r", encoding="utf-8") as f:
                raw = json.load(f)
            return [Student.from_dict(s) for s in raw]
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"[load_students] Error: {e}")
            return []

    def save_students(self) -> None:
        """Write the current student list back to the JSON file."""
        try:
            with open(self.FILE_NAME, "w", encoding="utf-8") as f:
                json.dump([s.to_dict() for s in self.students], f, indent=4)
        except Exception as e:
            print(f"[save_students] Error: {e}")

    # -----------------------------
    # helpers to find/check things (Private)
    # -----------------------------
    def _find_student(self, student_id: str) -> Student | None:
        """Return the student with the given 6-digit id string, or None."""
        target = f"{int(student_id):06d}"
        for s in self.students:
            if s.id == target:
                return s
        return None

    def _email_available(self, email: str) -> bool:
        """Return True if this email is not already used in the DB."""
        return all(s.email.strip().lower() != email for s in self.students)

    def _generate_unique_student_id(self) -> str:
        """Generate a 6-digit ID not used by any student in the DB."""
        used = {s.id for s in self.students}
        while True:
            new_id = f"{random.randint(1, 999_999):06d}"
            if new_id not in used:
                return new_id

    def _generate_unique_subject_id(self, student: Student) -> str:
        """Generate a 3-digit subject id unique within this student's subject list."""
        used = {sub.id for sub in student.subjects}
        while True:
            new_id = f"{random.randint(1, 999):03d}"
            if new_id not in used:
                return new_id

    # -----------------------------
    # public actions (used by CLI/GUI(controller.py))
    # -----------------------------
    def add_student(self, email: str, password: str, name: str) -> str | None:
        """
        Create a new student and save the DB.
        Returns the new student id string, or None if email exists.
        (I assume validation for email/password is done before calling this.)
        """
        if not self._email_available(email):
            return None
        new_id = self._generate_unique_student_id()
        new_student = Student(email, password, name, [], new_id, 0.0, False)
        self.students.append(new_student)
        self.save_students()
        return new_id

    def change_password(self, student_id: str, new_password: str) -> bool:
        """
        Update the password for a student if the id exists.
        I expect the caller to validate the password format first.
        """
        stu = self._find_student(student_id)
        if not stu:
            print("Student ID not found.")
            return False
        stu.password = new_password
        self.save_students()
        return True

    def enrol(self, student_id: str) -> str:
        """
        Enrol the student into ONE subject with a random mark.
        Enforces the 4-subject limit.
        Returns a user-friendly message for CLI.
        """
        stu = self._find_student(student_id)
        if not stu:
            return "Student ID not found."

        if len(stu.subjects) >= 4:
            return "Students are allowed to enrol in 4 subjects only."

        # Create a new subject with unique ID and random mark 25..100
        new_sub_id = self._generate_unique_subject_id(stu)
        new_mark = random.randint(25, 100)
        stu.subjects.append(Subject(new_sub_id, new_mark))

        # Recompute overall + status, then save
        stu._recompute_overall_and_status()
        self.save_students()

        return (f"Enrolling in Subject-{new_sub_id}\n"
                f"You are now enrolled in {len(stu.subjects)} out of 4 subjects")

    def remove_subject(self, student_id: str, subject_id: str) -> str:
        """
        Remove one subject by its ID from the given student.
        Returns a message string for CLI display.
        """
        stu = self._find_student(student_id)
        if not stu:
            return "Student ID not found."

        target = f"{int(subject_id):03d}"
        before = len(stu.subjects)
        stu.subjects = [sub for sub in stu.subjects if sub.id != target]

        if len(stu.subjects) == before:
            return f"Subject {subject_id} does not exist"

        stu._recompute_overall_and_status()
        self.save_students()
        return (f"Dropping Subject {subject_id}\n"
                f"You are now enrolled in {len(stu.subjects)} out of 4 subjects")

    def list_subjects(self, student_id: str) -> list[Subject]:
        stu = self._find_student(student_id)
        return [] if not stu else stu.subjects

    def show_students(self, mode: int) -> None:
        """
        Print students according to mode:
          1 = simple list
          2 = group by overall grade (I print sorted by overall)
          3 = partition into FAIL / PASS buckets using overall >= 50
        """
        if len(self.students) == 0:
            print("     < Nothing to Display >")
            return

        if mode == 1:
            # Simple list
            for s in self.students:
                print(f"{s.name} : : {s.id} --> Email: {s.email}")

        elif mode == 2:
            # Group by grade (I print sorted by overall, showing the overall grade)
            sorted_students = sorted(self.students, key=lambda x: x.overall)
            for s in sorted_students:
                overall_grade = check_func.get_grade(s.overall)
                print(f"{overall_grade} --> [{s.name} : : {s.id} --> GRADE: {overall_grade} - MARK: {s.overall}]")

        else:
            # Partition into PASS/FAIL
            fails, passes = [], []
            for s in self.students:
                overall_grade = check_func.get_grade(s.overall)
                line = f"{s.name} : : {s.id} --> GRADE: {overall_grade} - MARK: {s.overall}"
                (passes if s.status else fails).append(line)

            print(f"FAIL --> {fails}")
            print(f"PASS --> {passes}")

    def remove_student(self, student_id: str) -> bool:
        """
        Remove a student by id. Returns True if removed, False if not found.
        """
        target = f"{int(student_id):06d}"
        for s in list(self.students):
            if s.id == target:
                self.students.remove(s)
                self.save_students()
                return True
        return False

    def remove_all(self) -> str:
        self.students = []
        self.save_students()
        return "Students data cleared"
    
    def check_db_email(self, email):
        """Return True if the email is available."""
        for stu in self.students:
            if stu.email.strip().lower() == email:
                return False
        return True