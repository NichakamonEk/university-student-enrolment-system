# Student Enrolment System

## Project Overview

This project implements a simple Student Enrolment Management System with both CLI (Command Line Interface) and GUI (Graphical User Interface) modes.

The system allows students to:

    - Register new accounts with email and password validation
    - Login and manage enrolments (add/remove subjects)
    - View enrolled subjects with marks and grades
    - Change their passwords

An administrator can also:

    - View, group, and partition students by performance
    - Remove students or clear all data
    - All student data are stored locally in a students.data file (JSON format).

All student data are stored locally in a `students.data` file (JSON format). 

---

## System Architecture

| Layer                         | File                                                  | Description                                                                 |
|------------------------------|-------------------------------------------------------|-----------------------------------------------------------------------------|
| 1. Validation & Utilities    | check_func.py                                         | Helper functions for validating email/password, grading, and generating IDs |
| 2. Data Models               | classes.py                                            | Defines Subject, Student, and Database classes; manages JSON read/write     |
| 3. Logic Controller          | controllers.py                                        | Handles application logic and connects UI actions to the Database           |
| 4. CLI Interface             | main.py                                               | Command-line interface for student and admin operations                     |
| 5. GUI Interfaces            | login_page.py, register_page.py, enroll_page.py       | Tkinter-based GUI for login, registration, and enrolment management         |
| 6. Notes                     | classes_design_note.txt, GUI_note.txt                 | Design documentation for data flow and interface behaviour                  |

---

## System Requirements

- **Python Version:** 3.10 or higher  
- **Libraries:**  
  - `tkinter` (built-in with Python)  
  - `json`, `random`, `os`, `re` (all standard Python libraries)  

No external dependencies are required.

---

## Installation & Setup

1. **Clone or Copy** all source files into a single folder.  

2. Ensure the folder includes:
    - **`main.py`**
    - **`classes.py`** 
    - **`check_func.py`**
    - **`controllers.py`**
    - **`login_page.py`** 
    - **`register_page.py`**
    - **`enroll_page.py`**
    - **`students.data`**
    - **`classes_design_note.txt`**

3. The file `students.data` will automatically be created or updated when you run the program.

---

## Configuration

- No additional configuration is required.  
- The system automatically stores data in the same directory as the Python files.  
- Default data file: `students.data` (JSON format).  

## How to Run

### Option 1 – **CLI Mode**
Run in terminal:
- python **`main.py`**
- Choose (A) for Admin or (S) for Student
- Students can login or register, enrol subjects, and view marks.
- Admin can group, partition, or remove students.


### Option 2 – **GUI Mode**
Run in terminal:
- python **`login_page.py`**
- Opens the Tkinter login window.
- Use “Register now” to create a new student.
- After login, you can enrol, view, or remove subjects, and change password.
