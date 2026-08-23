from tkinter import messagebox
from ui.flight_booking import FlightBookingWindow

def handle_booking(flight_id, seat_number):
    messagebox.showinfo("Booked", f"Flight {flight_id}, Seat {seat_number} booked!")

def run_flight_booking():
    FlightBookingWindow(handle_booking)
