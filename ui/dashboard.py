import tkinter as tk
from tkinter import messagebox, ttk
from utils.pdf_generator import generate_ticket
import mysql.connector
from ui.payment import PaymentWindow



class DashboardWindow:
    def __init__(self, username):
        self.username = username
        self.window = tk.Tk()
        self.window.title("Dashboard")
        self.setup_ui()
        self.search_flights()
        self.window.mainloop()

    def setup_ui(self):
        tk.Label(self.window, text=f"Welcome, {self.username}!", font=("Helvetica", 16)).pack(pady=10)

        # Search Frame
        search_frame = tk.Frame(self.window)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="From:").grid(row=0, column=0)
        self.origin_entry = tk.Entry(search_frame)
        self.origin_entry.grid(row=0, column=1)

        tk.Label(search_frame, text="To:").grid(row=0, column=2)
        self.destination_entry = tk.Entry(search_frame)
        self.destination_entry.grid(row=0, column=3)

        tk.Label(search_frame, text="From Date (YYYY-MM-DD):").grid(row=1, column=0)
        self.from_date_entry = tk.Entry(search_frame)
        self.from_date_entry.grid(row=1, column=1)

        tk.Label(search_frame, text="To Date (YYYY-MM-DD):").grid(row=1, column=2)
        self.to_date_entry = tk.Entry(search_frame)
        self.to_date_entry.grid(row=1, column=3)

        tk.Button(search_frame, text="Search Flights", command=self.search_flights).grid(row=0, column=4, rowspan=2, padx=10)

        # Booking Frame
        booking_frame = tk.Frame(self.window)
        booking_frame.pack(pady=10)

        #  Define the variable before using in the checkbox
        self.is_self_booking = tk.BooleanVar(value=False)

        self.is_self_booking = tk.BooleanVar(value=True)
        self.checkbox = tk.Checkbutton(booking_frame, text="Booking for someone else", variable=self.is_self_booking,
                                       command=self.toggle_passenger_fields)

        self.checkbox.grid(row=0, column=0, columnspan=2)

        # Horizontal booking fields in a single row
        self.passenger_name_label = tk.Label(booking_frame, text="Passenger Name:")
        self.passenger_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.passenger_name_entry = tk.Entry(booking_frame, width=12)
        self.passenger_name_entry.grid(row=1, column=1, padx=5)

        self.passenger_passport_label = tk.Label(booking_frame, text="Passport Number:")
        self.passenger_passport_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.passenger_passport_entry = tk.Entry(booking_frame, width=12)
        self.passenger_passport_entry.grid(row=1, column=3, padx=5)

        tk.Label(booking_frame, text="Seat Number:").grid(row=1, column=4, padx=5, pady=5, sticky="e")
        self.seat_entry = tk.Entry(booking_frame, width=6)
        self.seat_entry.grid(row=1, column=5, padx=5)

        # Initially hide these
        self.passenger_name_label.grid_remove()
        self.passenger_name_entry.grid_remove()
        self.passenger_passport_label.grid_remove()
        self.passenger_passport_entry.grid_remove()

        # Treeview
        columns = ("ID", "Flight", "From", "To", "Departure", "Arrival", "Seats", "Price")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=100)
        self.tree.pack(pady=10)

        tk.Button(self.window, text="Reserve Selected Flight", command=self.reserve_flight).pack(pady=5)
        tk.Button(self.window, text="View My Reservations", command=self.view_my_reservations).pack(pady=5)

    def toggle_passenger_fields(self):
        if self.is_self_booking.get():
            # Checkbox is checked → booking for someone else → show fields
            self.passenger_name_label.grid()
            self.passenger_name_entry.grid()
            self.passenger_passport_label.grid()
            self.passenger_passport_entry.grid()
        else:
            # Booking for self → hide the fields
            self.passenger_name_label.grid_remove()
            self.passenger_name_entry.grid_remove()
            self.passenger_passport_label.grid_remove()
            self.passenger_passport_entry.grid_remove()

    def search_flights(self):
        origin = self.origin_entry.get().strip().lower()
        destination = self.destination_entry.get().strip().lower()
        from_date = self.from_date_entry.get().strip()
        to_date = self.to_date_entry.get().strip()

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="ABOODabood533/1208", database="FlightDB")
            cursor = conn.cursor()
            query = """
                SELECT id, flight_number, origin, destination, departure_time,
                       arrival_time, seats_available, price
                FROM flights
            """
            #for filtring database according to user search
            filters = []
            params = []

            if origin:
                filters.append("LOWER(origin) LIKE %s")
                params.append(f"%{origin}%")
            if destination:
                filters.append("LOWER(destination) LIKE %s")
                params.append(f"%{destination}%")
            if from_date:
                filters.append("DATE(departure_time) >= %s")
                params.append(from_date)
            if to_date:
                filters.append("DATE(departure_time) <= %s")
                params.append(to_date)

            if filters:
                query += " WHERE " + " AND ".join(filters)

            cursor.execute(query, params)
            flights = cursor.fetchall()
            conn.close()

            self.tree.delete(*self.tree.get_children())
            for flight in flights:
                self.tree.insert("", tk.END, values=flight)

            if not flights:
                messagebox.showinfo("No Flights", "No matching flights found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def reserve_flight(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a flight to reserve.")
            return

        flight_data = self.tree.item(selected)["values"]
        flight_id = flight_data[0]

        seat_number = self.seat_entry.get().strip()
        if not seat_number:
            messagebox.showwarning("Missing Info", "Please enter seat number.")
            return

        #  Call this only after payment is confirmed
        def proceed_after_payment():
            self._finalize_reservation(flight_id, seat_number)

        #  Show payment window and proceed if paid
        PaymentWindow(on_payment_success=proceed_after_payment)




    def view_my_reservations(self):
        def download_ticket():
            selected = res_tree.focus()
            if not selected:
                messagebox.showwarning("No Selection", "Please select a reservation.")
                return
            data = res_tree.item(selected)["values"]
            generate_ticket(
                reservation_id=data[0],
                passenger_name=data[6],
                flight_number=data[1],
                origin=data[2],
                destination=data[3],
                departure=data[4],
                seat=data[9],
                price=data[8]
            )

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="ABOODabood533/1208", database="FlightDB")
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
            user = cursor.fetchone()
            if not user:
                messagebox.showerror("Error", "User not found.")
                return
            user_id = user[0]

            cursor.execute("""
                SELECT r.id, f.flight_number, f.origin, f.destination, f.departure_time,
                       f.arrival_time, r.passenger_name, r.passenger_passport, f.price, r.seat_number
                FROM reservations r
                JOIN flights f ON r.flight_id = f.id
                WHERE r.user_id = %s
            """, (user_id,))
            reservations = cursor.fetchall()
            conn.close()

            res_win = tk.Toplevel(self.window)
            res_win.title("My Reservations")

            columns = ("ID", "Flight", "From", "To", "Departure", "Arrival", "Name", "Passport", "Price", "Seat")
            res_tree = ttk.Treeview(res_win, columns=columns, show="headings")
            for col in columns:
                res_tree.heading(col, text=col)
                res_tree.column(col, anchor=tk.CENTER, width=100)
            res_tree.pack(padx=10, pady=10)

            tk.Button(res_win, text="Download Ticket PDF", command=download_ticket).pack(pady=5)
            for row in reservations:
                res_tree.insert("", tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def _finalize_reservation(self, flight_id, seat_number):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="ABOODabood533/1208",
                                           database="FlightDB")
            cursor = conn.cursor()

            cursor.execute("SELECT id, passport FROM users WHERE username = %s", (self.username,))
            user = cursor.fetchone()
            if not user:
                messagebox.showerror("Error", "User not found.")
                return
            user_id, passport = user

            if self.is_self_booking.get():
                cursor.execute("""
                    SELECT * FROM reservations 
                    WHERE user_id = %s AND flight_id = %s AND passenger_name = %s AND passenger_passport = %s
                """, (user_id, flight_id, self.username, passport))
                if cursor.fetchone():
                    messagebox.showinfo("Already Reserved", "You already reserved this flight.")
                    return

                cursor.execute("""
                    INSERT INTO reservations (user_id, flight_id, seat_number, passenger_name, passenger_passport)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, flight_id, seat_number, self.username, passport))
            else:
                name = self.passenger_name_entry.get().strip()
                passport_num = self.passenger_passport_entry.get().strip()
                if not name or not passport_num:
                    messagebox.showwarning("Missing Info", "Please enter passenger name and passport number.")
                    return

                cursor.execute("""
                    SELECT * FROM reservations 
                    WHERE flight_id = %s AND passenger_name = %s AND passenger_passport = %s
                """, (flight_id, name, passport_num))
                if cursor.fetchone():
                    messagebox.showinfo("Already Reserved", f"{name} is already reserved on this flight.")
                    return

                cursor.execute("""
                    INSERT INTO reservations (user_id, flight_id, seat_number, passenger_name, passenger_passport)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, flight_id, seat_number, name, passport_num))

            cursor.execute("UPDATE flights SET seats_available = seats_available - 1 WHERE id = %s", (flight_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Flight reserved successfully!")
            self.search_flights()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
