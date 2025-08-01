from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid

from services.flight_service import FlightService
from services.luggage_service import LuggageService
from services.meal_service import MealService
from services.payment_service import PaymentService
from log_manager import log, get_logs

app = FastAPI()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

class BookingRequest(BaseModel):
    user_id: str
    simulate_meal_failure: bool = False

@app.post("/book_flight")
async def book_flight(request: BookingRequest):
    booking_id = str(uuid.uuid4())[:8]
    log(f"📦 Booking started for user {request.user_id} [ID: {booking_id}]")

    try:
        FlightService.book_flight(booking_id)
        LuggageService.add_luggage(booking_id)

        if request.simulate_meal_failure:
            raise Exception("Simulated meal service failure")

        MealService.add_meal(booking_id)
        PaymentService.process_payment(booking_id)

        log(f"✅ Booking successful for {booking_id}")
        return {"status": "SUCCESS", "booking_id": booking_id}

    except Exception as e:
        log(f"❌ Booking failed for {booking_id}: {e}")
        PaymentService.rollback(booking_id)
        MealService.rollback(booking_id)
        LuggageService.rollback(booking_id)
        FlightService.rollback(booking_id)

        return JSONResponse(status_code=500, content={
            "status": "FAILED",
            "reason": str(e),
            "booking_id": booking_id
        })

@app.get("/logs")
def fetch_logs():
    return {"logs": get_logs()}
