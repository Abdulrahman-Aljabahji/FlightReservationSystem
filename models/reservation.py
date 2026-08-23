class Reservation:
    def __init__(self, reservation_id, user_id, flight_id, passenger_name, passenger_passport):
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.flight_id = flight_id
        self.passenger_name = passenger_name
        self.passenger_passport = passenger_passport

    def __str__(self):
        return f"Reservation for {self.passenger_name}, Flight ID: {self.flight_id}"
