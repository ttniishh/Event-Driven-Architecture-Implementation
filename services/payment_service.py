from log_manager import log

class PaymentService:
    @staticmethod
    def process_payment(booking_id: str, force_fail: bool = False):
        log(f"[{booking_id}] Processing payment")
        if force_fail:
            raise Exception("Simulated payment failure (demo)")
        log(f"[{booking_id}] Payment processed successfully")

    @staticmethod
    def rollback(booking_id: str):
        log(f"[{booking_id}] Payment refunded (rollback)")
