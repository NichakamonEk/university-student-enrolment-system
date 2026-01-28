"""
login_page.py
-------------
GUI login window for GUIUniApp.

Design:
- GUI only talks to controllers.py (not directly to classes.Database()).
- We validate inputs (empty, regex) before calling controllers.login().
- On success, we open the enrolment window and hide this login window.
"""

from tkinter import *
from tkinter import ttk, messagebox
import check_func
import controllers          # <- our layer
from enroll_page import enroll_window
from register_page import register_window


def build_login_window():
    """Create and return the login Tk root window."""
    root = Tk()
    root.title("GUIUniApp")
    root.geometry("300x200")
    root.resizable(False, False)

    # ---- widgets
    ttk.Label(root, text="Email").place(x=20, y=20)
    username_entry = ttk.Entry(root)
    username_entry.place(x=100, y=20, width=150)

    ttk.Label(root, text="Password").place(x=20, y=60)
    password_entry = ttk.Entry(root, show="*")
    password_entry.place(x=100, y=60, width=150)

    # event handlers use closures over the entry widgets
    def handle_login():
        email = (username_entry.get() or "").strip()
        pw = (password_entry.get() or "").strip()

        # 1) empty check
        if not email or not pw:
            messagebox.showerror("Login Failed", "Fields should not be empty")
            return

        # 2) format check
        if not check_func.check_email(email) or not check_func.check_password(pw):
            messagebox.showerror("Login Failed", "Incorrect email or password format")
            return

        # 3) attempt login via controllers
        student = controllers.login(email, pw)
        if student is None:
            # either email not found or wrong password
            # (controllers.login checks both together)
            messagebox.showerror("Login Failed", "Student doesn't exist or password is incorrect")
            return

        # 4) success: open enrolment window and hide login
        root.withdraw()
        enroll_window(root, student)

    def handle_register():
        root.withdraw()
        register_window(root)

    # buttons / links
    ttk.Button(root, text="Login", command=handle_login).place(x=120, y=100)

    Label(root, text="Don't have an account?").place(x=40, y=140)
    Button(root, text="Register now", fg="blue", cursor="hand2",
           relief=FLAT, command=handle_register).place(x=170, y=138)

    # enable pressing Enter to login
    root.bind("<Return>", lambda _e: handle_login())

    return root


# Run directly
if __name__ == "__main__":
    app = build_login_window()
    app.mainloop()
