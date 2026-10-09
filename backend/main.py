from datetime import date
from database import get_connection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date, time
from validators import has_reached_booking_limit

app = FastAPI()


class BookingRequest(BaseModel):
    member_id: int
    facility_id: int
    date: date
    start_time: str  # e.g. "18:00"


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/facilities")
def list_facilities():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, weekday_price, weekend_price FROM facilities ORDER BY id")
            rows = cur.fetchall()
    finally:
        conn.close()
    return [
        {"id": r[0], "name": r[1], "weekday_price": r[2], "weekend_price": r[3]}
        for r in rows
    ]
@app.get("/slots")
def list_slots(facility_id: int, date: date):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT start_time FROM bookings WHERE facility_id = %s AND booking_date = %s",
                (facility_id, date),
            )
            booked = {row[0] for row in cur.fetchall()}
    finally:
        conn.close()

    slots = []
    for hour in range(6, 22):  # start times 6 AM to 9 PM = 16 slots
        start = time(hour, 0)
        slots.append({
            "start_time": start.strftime("%H:%M"),
            "status": "booked" if start in booked else "available",
        })
    return slots


@app.post("/bookings")
def create_booking(request: BookingRequest):
    fake_active_count = 3  # hardcoded for now, real count comes from the DB on Day 3
    if has_reached_booking_limit(fake_active_count):
        raise HTTPException(status_code=400, detail="Member already has 3 active bookings")
    return {"id": 1, "status": "confirmed", **request.model_dump(mode="json")}


@app.get("/bookings")
def list_member_bookings(member_id: int):
    return [
        {"id": 1, "member_id": member_id, "facility_id": 1,
         "date": "2026-10-12", "start_time": "18:00"}
    ]