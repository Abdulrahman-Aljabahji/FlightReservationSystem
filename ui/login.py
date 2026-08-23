import tkinter as tk

class LoginWindow:
    def __init__(self, on_login, on_register):
        self.on_login = on_login
        self.on_register = on_register
        self.window = tk.Tk()
        self.window.title("Login")
        self.build_ui()

    def build_ui(self):
        frame = tk.Frame(self.window)
        frame.pack(padx=20, pady=20)

        # Username
        tk.Label(frame, text="Username").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password
        tk.Label(frame, text="Password").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        #  Admin checkbox
        self.is_admin = tk.BooleanVar()
        admin_checkbox = tk.Checkbutton(frame, text="Login as Admin", variable=self.is_admin)
        admin_checkbox.grid(row=2, columnspan=2, pady=(0, 10))

        #  Login button (includes is_admin)
        tk.Button(frame, text="Login", command=self.login).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Register", command=self.on_register).grid(row=3, column=1, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        is_admin = self.is_admin.get()  #  Get admin checkbox value
        self.on_login(username, password, is_admin)

    def run(self):
        self.window.mainloop()
