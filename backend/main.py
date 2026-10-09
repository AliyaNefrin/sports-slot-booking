from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    return [
        {"id": 1, "name": "Badminton Court 1"},
        {"id": 2, "name": "Badminton Court 2"},
        {"id": 3, "name": "Tennis Court"},
    ]


@app.get("/slots")
def list_slots(facility_id: int, date: date):
    return [
        {"start_time": "06:00", "status": "available"},
        {"start_time": "07:00", "status": "booked"},
        {"start_time": "08:00", "status": "available"},
    ]


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