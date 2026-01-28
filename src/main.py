"""
main.py — CLI entry for CLIUniApp

Connects:
- check_func.py   validation (email/password)
- classes.py      Student, Subject, Database ** Read classes_design_note**
"""

import check_func
import classes

# One shared database instance for this file
database = classes.Database()


# -------------------------
#  START
# -------------------------
def main():
    print("Welcome to CLIUniApp")
    show_cli()


# -------------------------
#  UNIVERSITY MAIN MENU
# -------------------------
def show_cli():
    while True:
        option = input("University System: (A)dmin, (S)tudent, or (X)exit: ").strip().upper()
        if option == "A":
            admin_cli()
        elif option == "S":
            student_cli()
        elif option == "X":
            print("Thank you for using CLIUniApp!")
            break
        else:
            print("Invalid option, please try again.")


# -------------------------
#  STUDENT MENU
# -------------------------
def student_cli():
    """(l)ogin, (r)egister, e(x)it"""
    while True:
        option = input("Student System (l/r/x): ").strip().lower()
        if option == "l":
            login_cli()
        elif option == "r":
            register_cli()
        elif option == "x":
            print("Returning to main menu...")
            return
        else:
            print("Invalid option, please try again.")


# -------------------------
#  REGISTER
# -------------------------
def register_cli():
    print("\n=== Student Registration ===")
    while True:
        email = input("Email: ").strip().lower()
        password = input("Password: ")

        # 1) format checks
        if not (check_func.check_email(email) and check_func.check_password(password)):
            print("Incorrect email or password format.")
            continue

        # 2) email exists?
        if not database.check_db_email(email):
            print("This email already exists. Please try login instead.")
            return

        # 3) create
        name = input("Full Name: ").strip()
        database.add_student(email, password, name)
        print(f"Student {name} registered successfully!\n")
        return


# -------------------------
#  LOGIN
# -------------------------
def login_cli():
    print("\n=== Student Login ===")

    # always refresh from disk before login
    database.students = database.load_students()

    email = input("Email: ").strip().lower()
    password = input("Password: ")

    if not (check_func.check_email(email) and check_func.check_password(password)):
        print("Incorrect email or password format.")
        return

    student = next((stu for stu in database.students if stu.email.strip().lower() == email), None)
    if not student:
        print("Student not found.")
        return
    if student.password != password:
        print("Incorrect password.")
        return

    print(f"Welcome, {student.name}!")
    subject_enrolment_cli(student)


# -------------------------
#  ENROLMENT (after login)
# -------------------------
def subject_enrolment_cli(student):
    """Manage subjects: change pw / enrol / remove / show / exit."""
    global database  # we’ll re-use the shared DB

    print("\n=== Subject Enrolment Menu ===")
    while True:
        option = input("Student Menu (c/e/r/s/x): ").strip().lower()

        if option == "c":
            new_pw = input("Enter new password: ").strip()
            confirm = input("Confirm new password: ").strip()
            while new_pw != confirm:
                print("Passwords do not match! Try again.")
                confirm = input("Confirm new password: ").strip()
            if not check_func.check_password(new_pw):
                print("Invalid password format.")
                continue
            ok = database.change_password(student.id, new_pw)
            print("Password updated successfully." if ok else "Student not found.")

        elif option == "e":
            # CALL THE DATABASE METHOD (enrol)
            msg = database.enrol(student.id)
            print(msg)
            # refresh local copy of student
            student = next((s for s in database.students if s.id == student.id), student)

        elif option == "r":
            subject_id = input("Enter subject ID to remove (e.g., 001): ").strip()
            msg = database.remove_subject(student.id, subject_id)
            print(msg)
            # refresh local copy
            student = next((s for s in database.students if s.id == student.id), student)

        elif option == "s":
            subs = database.list_subjects(student.id)
            if not subs:
                print("Showing 0 subjects")
            else:
                print(f"Showing {len(subs)} subjects\n")
                for sub in subs:
                    print(f"[ Subject::{sub.id} -- mark = {sub.mark} -- grade = {sub.grade} ]")

        elif option == "x":
            print("Logging out...")
            return

        else:
            print("Invalid option, please try again.")


# -------------------------
#  ADMIN
# -------------------------
def admin_cli():
    print("\n=== Admin System ===")
    while True:
        option = input(" Admin Menu (c/g/p/r/s/x): ").strip().lower()

        if option == "c":
            confirm = input("Are you sure to clear all student data? (y/n): ").strip().lower()
            if confirm == "y":
                database.remove_all()
                print("All student data cleared!")
            else:
                print("Cancelled.")

        elif option == "g":
            print("Group students by grade:")
            database.show_students(2)

        elif option == "p":
            print("Partition students (PASS/FAIL):")
            database.show_students(3)

        elif option == "r":
            student_id = input("Enter Student ID to remove: ").strip()
            if not database.remove_student(student_id):
                print("Student not found.")
            else:
                print(f"Student {student_id} removed.")

        elif option == "s":
            print("List of students:")
            database.show_students(1)

        elif option == "x":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option, please try again.")


# -------------------------
#  RUN
# -------------------------
if __name__ == "__main__":
    main()
