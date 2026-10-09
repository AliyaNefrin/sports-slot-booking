from dataclasses import dataclass
from datetime import date, time


@dataclass
class Facility:
    id: int
    name: str
    weekday_price: int
    weekend_price: int


@dataclass
class Booking:
    id: int
    member_id: int
    facility_id: int
    booking_date: date
    start_time: time