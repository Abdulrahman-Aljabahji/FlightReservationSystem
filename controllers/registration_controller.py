from tkinter import messagebox
from ui.registration import RegistrationWindow
import bcrypt
import mysql.connector

class RegistrationController:
    def __init__(self):
        self.window = RegistrationWindow(self.handle_register)

    def handle_register(self, passport, username, email, password):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ABOODabood533/1208",
                database="FlightDB",
                port=3306
            )
            cursor = conn.cursor()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO users (passport, username, email, password) VALUES (%s, %s, %s, %s)",
                (passport, username, email, hashed_password)
            )

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration successful!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")

def open_registration_window():
    RegistrationController()
