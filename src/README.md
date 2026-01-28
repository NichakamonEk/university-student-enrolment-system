# How to Run the Student Enrolment System

This folder contains the source code for the university student enrolment system.

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
