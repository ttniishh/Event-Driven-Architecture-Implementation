from log_manager import log

class PaymentService:
    @staticmethod
    def process_payment(booking_id: str):
        log(f"[{booking_id}] Payment processed")

    @staticmethod
    def rollback(booking_id: str):
        log(f"[{booking_id}] Payment refunded (rollback)")
