from log_manager import log

class MealService:
    @staticmethod
    def add_meal(booking_id: str, meal: str):
        log(f"[{booking_id}] Meal preference added: {meal}")

    @staticmethod
    def rollback(booking_id: str):
        log(f"[{booking_id}] Meal preference rolled back")
