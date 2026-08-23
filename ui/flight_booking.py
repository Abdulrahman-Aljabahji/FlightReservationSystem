import tkinter as tk

class FlightBookingWindow:
    def __init__(self, on_book):
        self.on_book = on_book
        self.window = tk.Toplevel()
        self.window.title("Book a Flight")
        self.build_ui()

    def build_ui(self):
        tk.Label(self.window, text="Flight ID").pack()
        self.flight_entry = tk.Entry(self.window)
        self.flight_entry.pack()

        tk.Label(self.window, text="Seat Number").pack()
        self.seat_entry = tk.Entry(self.window)
        self.seat_entry.pack()

        tk.Button(self.window, text="Book", command=self.book).pack()

    def book(self):
        flight_id = self.flight_entry.get()
        seat_number = self.seat_entry.get()
        self.on_book(flight_id, seat_number)
