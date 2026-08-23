class Flight:
    def __init__(self, flight_id, flight_number, origin, destination, departure_time, arrival_time, seats_available, price):
        self.flight_id = flight_id
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.seats_available = seats_available
        self.price = price

    def __str__(self):
        return f"{self.flight_number}: {self.origin} to {self.destination}"
