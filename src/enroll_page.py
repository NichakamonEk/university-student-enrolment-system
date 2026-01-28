"""
enroll_page.py
---------------
Tkinter window for a logged-in student to manage enrolments.

Design choices:
- This GUI calls functions in controllers.py (not classes.Database directly).
- After each action (enrol/remove/change password), we fetch fresh data.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import controllers  # our logic layer, not mess with classes.py

def _fetch_student_by_email(email):
    """
    Helper: get a fresh Student object by email.
    Because controllers.login(email, pw) needs a password, we loop the DB here.
    """
    for stu in controllers.db.students:
        if stu.email == email:
            return stu
    return None

def _refresh_student(student):
    """Return the latest copy of this student from the DB by ID."""
    # controllers keeps db in memory; reload the reference each time to avoid stale data
    sid = student.id
    for stu in controllers.db.students:
        if stu.id == sid:
            return stu
    return None

def show_subjects(student):
    """Show the current list of enrolled subjects in a messagebox."""
    fresh = _refresh_student(student)
    if not fresh:
        messagebox.showerror("Error", "Student not found.")
        return

    subs = controllers.db.list_subjects(fresh.id)
    if not subs:
        messagebox.showinfo("Subjects", "Showing 0 subjects")
        return

    lines = [f"Showing {len(subs)} subjects", ""]
    for s in subs:
        lines.append(f"[ Subject::{s.id} -- mark = {s.mark} -- grade = {s.grade} ]")
    messagebox.showinfo("Subjects", "\n".join(lines))

def enrol_one(student):
    """Ask controllers to enrol one new subject (max 4). Show the result message."""
    fresh = _refresh_student(student)
    if not fresh:
        messagebox.showerror("Error", "Student not found.")
        return

    result = controllers.enrol_subject(fresh.id)
    # controllers.enrol_subject returns message string
    messagebox.showinfo("Enrollment", result)

def remove_subject(student):
    """Prompt for a subject ID and remove it via controllers."""
    fresh = _refresh_student(student)
    if not fresh:
        messagebox.showerror("Error", "Student not found.")
        return

    sub_id = simpledialog.askstring("Remove Subject", "Enter Subject ID (e.g., 001):")
    if not sub_id:
        return  # user cancelled
    msg = controllers.remove_subject(fresh.id, sub_id.strip())
    messagebox.showinfo("Remove Subject", msg)

def change_password(student):
    """Prompt for a new password and update it via controllers (with validation)."""
    fresh = _refresh_student(student)
    if not fresh:
        messagebox.showerror("Error", "Student not found.")
        return

    new_pw = simpledialog.askstring("Change Password", "Enter new password:", show="*")
    if not new_pw:
        return
    msg = controllers.change_password(fresh.id, new_pw.strip())
    # controllers.change_password returns a message or validation error
    if "Invalid" in msg:
        messagebox.showerror("Change Password", msg)
    else:
        messagebox.showinfo("Change Password", msg)

def enroll_window(parent, student):
    """
    Open the enrolment window.
    'student' is the object returned by controllers.login(email, password).
    """
    # We’ll keep a reference to the student (and refresh before each action)
    current_student = student

    win = tk.Toplevel(parent)
    win.title("Enrollment Page")
    win.geometry("320x240")
    win.resizable(False, False)

    # When user closes this window, show the parent again (login/home)
    def _on_close():
        win.destroy()
        try:
            parent.deiconify()
        except Exception:
            pass

    win.protocol("WM_DELETE_WINDOW", _on_close)

    tk.Label(win, text=f"Welcome, {current_student.name}!", font=("Arial", 14)).pack(pady=10)

    tk.Button(
        win, text="Enroll", width=20,
        command=lambda: enrol_one(current_student)
    ).pack(pady=4)

    tk.Button(
        win, text="Show Subjects", width=20,
        command=lambda: show_subjects(current_student)
    ).pack(pady=4)

    tk.Button(
        win, text="Remove Subject", width=20,
        command=lambda: remove_subject(current_student)
    ).pack(pady=4)

    tk.Button(
        win, text="Change Password", width=20,
        command=lambda: change_password(current_student)
    ).pack(pady=4)

    tk.Button(
        win, text="Close", width=20,
        command=_on_close
    ).pack(pady=8)