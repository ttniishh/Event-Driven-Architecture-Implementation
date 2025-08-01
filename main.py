from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from services.flight_service import FlightService
from services.luggage_service import LuggageService
from services.meal_service import MealService
from services.payment_service import PaymentService
from log_manager import log, get_logs
import uuid

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class BookingRequest(BaseModel):
    user_id: str
    simulate_flight_failure: bool = False
    simulate_luggage_failure: bool = False
    simulate_meal_failure: bool = False
    simulate_payment_failure: bool = False


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/logs")
def get_log_file():
    return JSONResponse(content={"logs": get_logs()})


@app.post("/book_flight")
async def book_flight(request: BookingRequest):
    booking_id = str(uuid.uuid4())[:8]
    log(f"[{booking_id}] Booking started for {request.user_id}")

    try:
        # Flight
        if request.simulate_flight_failure:
            raise Exception("Simulated flight service failure")
        FlightService.book_flight(booking_id)

        # Luggage
        if request.simulate_luggage_failure:
            raise Exception("Simulated luggage service failure")
        LuggageService.add_luggage(booking_id)

        # Meal
        if request.simulate_meal_failure:
            raise Exception("Simulated meal service failure")
        MealService.add_meal(booking_id)

        # Payment
        if request.simulate_payment_failure:
            raise Exception("Simulated payment service failure")
        PaymentService.process_payment(booking_id)

        log(f"[{booking_id}] Booking completed successfully")

    except Exception as e:
        log(f"[{booking_id}] Error: {str(e)}")
        log(f"[{booking_id}] Initiating rollback")

        # Rollback in reverse order
        PaymentService.rollback(booking_id)
        MealService.rollback(booking_id)
        LuggageService.rollback(booking_id)
        FlightService.rollback(booking_id)

        log(f"[{booking_id}] Rollback completed")
    return {"status": "done"}
