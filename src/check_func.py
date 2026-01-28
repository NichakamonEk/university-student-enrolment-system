"""
check_func.py
-------------
This file contains helper functions for:
1. Grading marks
2. Checking valid email and password formats
3. Generating random IDs for students and subjects

Nicha: Checked
"""

# Import built-in Python libraries

import json
import os
import random
import re

# 1. Calculate grade from a mark

def get_grade(mark):
    """
    Decide the grade based on the mark.
    HD = 85+, D = 75–84, C = 65–74, P = 50–64, Z = below 50.
    """
    if mark >= 85:
        return "HD"
    elif mark >= 75:
        return "D"
    elif mark >= 65:
        return "C"
    elif mark >= 50:
        return "P"
    else:
        return "Z"

# 2. Validate student's email format

def check_email(email):
    """
    Check format:
    firstname.lastname@university.com
    Only letters are allowed for firstname and lastname.
    """
    pattern = r'^[a-z]+\.[a-z]+@university\.com$'
    # Convert to lowercase so it accepts uppercase input too
    email = email.lower()
    # re.match() returns a Match object if pattern is correct, otherwise None
    return bool(re.match(pattern, email))

# 3. Validate a student's password format

def check_password(password):
    """
    Check if the password follows these rules:
    1. Starts with an uppercase letter
    2. Has at least 5 more letters (total letters ≥ 6)
    3. Ends with at least 3 digits
    Example: HelloWorld1234
    """
    pattern = r'^[A-Z][a-zA-Z]{5,}[0-9]{3,}$'
    return bool(re.match(pattern, password))

# 4. Generate unique Student and Subject IDs

def generate_student_id(existing_ids):
    """
    Create a unique 6-digit student ID, e.g. '000123'.
    Avoids duplicates by checking existing IDs.
    """
    while True:
        new_id = f"{random.randint(1, 999999):06d}"
        if new_id not in existing_ids:
            return new_id

def generate_subject_id(existing_ids):
    """
    Create a unique 3-digit subject ID, e.g. '005'.
    Avoids duplicates for the same student.
    """
    while True:
        new_id = f"{random.randint(1, 999):03d}"
        if new_id not in existing_ids:
            return new_id
        
