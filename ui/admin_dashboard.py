import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class AdminDashboard:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Admin Dashboard")

        tk.Label(self.window, text="All Reservations", font=("Helvetica", 16)).pack(pady=10)

        columns = ("ID", "User", "Flight", "From", "To", "Departure", "Arrival", "Name", "Passport", "Seat", "Status", "Price")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=100)
        self.tree.pack(padx=10, pady=10)

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="View Flights", command=self.view_flights).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Add Flight", command=self.add_flight).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Reservation", command=self.delete_reservation).grid(row=0, column=2, padx=5)

        self.load_reservations()
        self.window.mainloop()

    def load_reservations(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ABOODabood533/1208",
                database="FlightDB"
            )
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.id, u.username, f.flight_number, f.origin, f.destination,
                       f.departure_time, f.arrival_time, r.passenger_name, r.passenger_passport,
                       r.seat_number, f.price
                FROM reservations r
                JOIN users u ON r.user_id = u.id
                JOIN flights f ON r.flight_id = f.id
            """)
            rows = cursor.fetchall()
            conn.close()

            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", tk.END, values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def delete_reservation(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a reservation to delete.")
            return

        res_id = self.tree.item(selected)["values"][0]
        confirm = messagebox.askyesno("Confirm", f"Delete reservation ID {res_id}?")
        if confirm:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="ABOODabood533/1208",
                    database="FlightDB"
                )
                cursor = conn.cursor()
                cursor.execute("DELETE FROM reservations WHERE id = %s", (res_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Deleted", "Reservation deleted successfully.")
                self.load_reservations()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", str(err))

    def view_flights(self):
        flights_win = tk.Toplevel(self.window)
        flights_win.title("All Flights")

        tree = ttk.Treeview(flights_win,
                            columns=("ID", "Flight No", "Origin", "Destination", "Departure", "Arrival", "Seats", "Price"),
                            show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        tree.pack(padx=10, pady=10)

        def load_flights():
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="ABOODabood533/1208",
                    database="FlightDB"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT id, flight_number, origin, destination, departure_time, arrival_time, seats_available, price FROM flights")
                rows = cursor.fetchall()
                conn.close()

                tree.delete(*tree.get_children())
                for row in rows:
                    tree.insert("", tk.END, values=row)

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

        def delete_flight():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a flight to delete.")
                return

            flight_id = tree.item(selected)['values'][0]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete flight ID {flight_id}?")
            if not confirm:
                return

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="ABOODabood533/1208",
                    database="FlightDB"
                )
                cursor = conn.cursor()
                cursor.execute("DELETE FROM flights WHERE id = %s", (flight_id,))
                conn.commit()
                conn.close()

                messagebox.showinfo("Deleted", "Flight deleted successfully.")
                load_flights()

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

        tk.Button(flights_win, text="Delete Selected Flight", command=delete_flight).pack(pady=5)
        load_flights()

    def add_flight(self):
        add_win = tk.Toplevel(self.window)
        add_win.title("Add New Flight")

        labels = ["Flight Number", "Origin", "Destination", "Departure Time (YYYY-MM-DD HH:MM)",
                  "Arrival Time (YYYY-MM-DD HH:MM)", "Seats Available", "Price"]
        entries = []

        for i, label_text in enumerate(labels):
            tk.Label(add_win, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(add_win)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        def save_flight():
            values = [e.get().strip() for e in entries]
            if any(v == "" for v in values):
                messagebox.showwarning("Missing Info", "Please fill in all fields.")
                return

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="ABOODabood533/1208",
                    database="FlightDB"
                )
                cursor = conn.cursor()
                cursor.execute("""
                               INSERT INTO flights (flight_number, origin, destination, departure_time,
                                                    arrival_time, seats_available, price)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)
                               """, tuple(values))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Flight added successfully.")
                add_win.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))

        tk.Button(add_win, text="Save", command=save_flight).grid(row=len(labels), columnspan=2, pady=10)
