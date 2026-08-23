from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def generate_ticket(reservation_id, passenger_name, flight_number, origin, destination, departure, seat, price):
    file_name = f"Ticket_{reservation_id}.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)

    text = c.beginText(50, 800)
    text.setFont("Helvetica-Bold", 14)
    text.textLine("✈️ Flight Ticket Confirmation")
    text.setFont("Helvetica", 12)
    text.textLine("")

    # Ticket info
    lines = [
        f"Reservation ID: {reservation_id}",
        f"Passenger Name: {passenger_name}",
        f"Flight Number: {flight_number}",
        f"Origin: {origin}",
        f"Destination: {destination}",
        f"Departure Time: {departure}",
        f"Seat: {seat}",
        f"Price: ${price}",
    ]

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()

    os.startfile(file_name) if os.name == 'nt' else os.system(f'open "{file_name}"')  # Auto-open on Mac/Win
