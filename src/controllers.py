"""
controllers.py
---------------
This file connects the menu buttons/GUI to the data logic.
It uses Database, Student, and Subject classes from classes.py
and the validation functions from check_func.py

Nicha: Final checked
"""

from classes import Database
import check_func

# Create a shared Database object
db = Database()

def register_student(email, password, name):

    """Register a new student if email and password are valid."""
    
    # 1. Validate email and password
    if not check_func.check_email(email):
        return "Invalid email format. Must end with @university.com"
    if not check_func.check_password(password):
        return "Invalid password format. Must start with uppercase, ≥5 letters, end with ≥3 digits"
    
    # 2. Add student to database
    student_id = db.add_student(email, password, name)
    if student_id is None:
        return "This email is already registered."
    
    return f"Registration successful! Your Student ID is {student_id}"


def login(email, password):
    """Find and return the student if credentials match."""
    for stu in db.students:
        if stu.email == email and stu.password == password:
            return stu
    return None


def enrol_subject(student_id):
    """Let the student enrol in a subject (max 4)."""
    return db.enrol(student_id)


def remove_subject(student_id, subject_id):
    """Remove one subject by ID."""
    return db.remove_subject(student_id, subject_id)


def change_password(student_id, new_password):
    """Change the student’s password if valid."""
    if not check_func.check_password(new_password):
        return "Invalid password format."
    success = db.change_password(student_id, new_password)
    return "Password updated successfully." if success else "Student not found."


def list_students(mode=1):
    """Show students (mode: 1=list, 2=group, 3=pass/fail)."""
    db.show_students(mode)


def remove_student(student_id):
    """Remove one student."""
    return "Removed." if db.remove_student(student_id) else "Student not found."


def clear_all():
    """Clear all student data (admin only)."""
    return db.remove_all()