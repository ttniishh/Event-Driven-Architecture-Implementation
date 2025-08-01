from log_manager import log

class FlightService:
    @staticmethod
    def book_flight(booking_id: str):
        log(f"[{booking_id}] Flight booked")

    @staticmethod
    def rollback(booking_id: str):
        log(f"[{booking_id}] Flight booking canceled (rollback)")
