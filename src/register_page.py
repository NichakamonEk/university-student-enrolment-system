"""
register_page.py
----------------
Tkinter window for student registration.

Flow:
- User types Name, Email, Password
- We validate (empty, email, password)
- We call controllers.register_student(email, password, name)
- On success: show ID and return to login
"""

from tkinter import *
from tkinter import ttk, messagebox
import check_func              # for email/password validation
import controllers             # for saving the new student to DB


def register_window(parent):
    """
    Opens the Register window as a child of the login window.
    When closing, we show login again
    """
    win = Toplevel(parent)
    win.title("Register")
    win.geometry("360x220")
    win.resizable(False, False)

    # If user clicks the window X, go back to login
    def _on_close():
        win.destroy()
        try:
            parent.deiconify()
        except Exception:
            pass

    win.protocol("WM_DELETE_WINDOW", _on_close)

    # -------- Form fields --------
    ttk.Label(win, text="Full Name").place(x=20, y=20)
    name_entry = ttk.Entry(win)
    name_entry.place(x=120, y=20, width=200)

    ttk.Label(win, text="Email").place(x=20, y=60)
    email_entry = ttk.Entry(win)
    email_entry.place(x=120, y=60, width=200)

    ttk.Label(win, text="Password").place(x=20, y=100)
    pw_entry = ttk.Entry(win, show="*")
    pw_entry.place(x=120, y=100, width=200)

    # -------- Handlers --------
    def handle_register():
        name = (name_entry.get() or "").strip()
        email = (email_entry.get() or "").strip()
        pw = (pw_entry.get() or "").strip()

        # 1) Empty checks
        if not name or not email or not pw:
            messagebox.showerror("Register Failed", "All fields are required.")
            return

        # 2) Local format checks
        if not check_func.check_email(email):
            messagebox.showerror("Register Failed", "Email must be like firstname.lastname@university.com")
            return
        if not check_func.check_password(pw):
            messagebox.showerror(
                "Register Failed",
                "Password must start with uppercase, have ≥5 letters, and end with ≥3 digits."
            )
            return

        # 3) Ask controllers to create the student
        #    It returns either a success message with ID or an error message.
        result = controllers.register_student(email, pw, name)

        if result.startswith("Registration successful"):
            messagebox.showinfo("Registered", result)
            _on_close()  # back to login
        else:
            messagebox.showerror("Register Failed", result)

    def handle_cancel():
        _on_close()

    ttk.Button(win, text="Register", command=handle_register).place(x=120, y=150, width=90)
    ttk.Button(win, text="Cancel", command=handle_cancel).place(x=230, y=150, width=90)

    # Press Enter to submit
    win.bind("<Return>", lambda _e: handle_register())

    # Focus the first field for convenience
    name_entry.focus_set()
