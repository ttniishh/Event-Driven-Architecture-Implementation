from log_manager import log

class MealService:
    @staticmethod
    def add_meal(booking_id: str):
        log(f"[{booking_id}] Meal added")

    @staticmethod
    def rollback(booking_id: str):
        log(f"[{booking_id}] Meal removed (rollback)")
