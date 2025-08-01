from log_manager import log

class LuggageService:
    @staticmethod
    def add_luggage(booking_id: str):
        log(f"[{booking_id}] Luggage added")

    @staticmethod
    def rollback(booking_id: str):
        log(f"[{booking_id}] Luggage removed (rollback)")
