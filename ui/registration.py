import tkinter as tk
from tkinter import messagebox

class RegistrationWindow:
    def __init__(self, on_register):
        self.on_register = on_register
        self.window = tk.Toplevel()
        self.window.title("Register")
        self.build_ui()

    def build_ui(self):
        tk.Label(self.window, text="Passport").grid(row=0, column=0)
        self.passport_entry = tk.Entry(self.window)
        self.passport_entry.grid(row=0, column=1)

        tk.Label(self.window, text="Username").grid(row=1, column=0)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.grid(row=1, column=1)

        tk.Label(self.window, text="Email").grid(row=2, column=0)
        self.email_entry = tk.Entry(self.window)
        self.email_entry.grid(row=2, column=1)

        tk.Label(self.window, text="Password").grid(row=3, column=0)
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.grid(row=3, column=1)

        tk.Button(self.window, text="Register", command=self.register).grid(row=4, columnspan=2, pady=10)

    def register(self):
        passport = self.passport_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not passport or not username or not email or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        self.on_register(passport, username, email, password)
