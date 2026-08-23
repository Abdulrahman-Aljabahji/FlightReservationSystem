from tkinter import messagebox
from ui.login import LoginWindow
from controllers.dashboard_controller import run_dashboard
from controllers.registration_controller import open_registration_window
import mysql.connector
import bcrypt
import tkinter as tk



def run_login():
    def handle_login(username, password, is_admin_checkbox):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ABOODabood533/1208",
                database="FlightDB"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()#fetchone selects one row
            conn.close()

            if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
                if is_admin_checkbox:
                    if user.get("is_admin"):
                        from controllers.admin_controller import run_admin_dashboard
                        run_admin_dashboard()
                    else:
                        tk.messagebox.showerror("Access Denied", "This user is not an admin.")
                else:
                    from ui.dashboard import DashboardWindow
                    DashboardWindow(username)
            else:
                tk.messagebox.showerror("Login Failed", "Invalid username or password.")

        except mysql.connector.Error as err:
            tk.messagebox.showerror("Database Error", f"{err}")

    def handle_register():
        open_registration_window()

    login_window = LoginWindow(handle_login, handle_register)
    login_window.run()
