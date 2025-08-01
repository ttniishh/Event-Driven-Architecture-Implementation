from fastapi import FastAPI, Form, Request
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

# Serve static files (index.html should be inside /static folder)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# For API calls using JSON
class BookingRequest(BaseModel):
    user_id: str
    flight_type: str
    luggage_needed: bool
    meal_preference: str
    force_fail: bool = False

@app.post("/book_flight")
async def book_flight(request: BookingRequest):
    return await handle_booking(
        user_id=request.user_id,
        flight_type=request.flight_type,
        luggage_needed=request.luggage_needed,
        meal_preference=request.meal_preference,
        force_fail=request.force_fail,
    )

# For form submissions from HTML UI
@app.post("/book_flight_form")
async def book_flight_form(
    name: str = Form(...),
    flight_type: str = Form("Economy"),
    luggage_needed: bool = Form(False),
    meal_preference: str = Form("No Meal"),
    force_fail: bool = Form(False)
):
    return await handle_booking(
        user_id=name,
        flight_type=flight_type,
        luggage_needed=luggage_needed,
        meal_preference=meal_preference,
        force_fail=force_fail,
    )

# Unified handler for both routes
async def handle_booking(user_id, flight_type, luggage_needed, meal_preference, force_fail):
    booking_id = str(uuid.uuid4())[:8]
    log(f"📦 Booking started for user {user_id} [ID: {booking_id}]")

    try:
        FlightService.book_flight(booking_id, flight_type)

        if luggage_needed:
            LuggageService.add_luggage(booking_id)

        if meal_preference != "No Meal":
            MealService.add_meal(booking_id, meal_preference)

        if force_fail:
            log(f"[{booking_id}] ⚠️ Simulating failure before payment.")
            raise Exception("Simulated payment failure")

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
