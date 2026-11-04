from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class FlightBase(BaseModel):
    # Regex валідація номера рейсу: 2 великі літери, дефіс, 3-4 цифри (наприклад, LH-101, PS-204)
    flight_number: str = Field(..., pattern=r"^[A-Z]{2}-\d{3,4}$")
    destination: str = Field(..., min_length=2, max_length=100)
    departure_date: date
    price: Decimal = Field(..., gt=0)
    flight_class: Literal["economy", "business"]
    has_seats: bool = True


class FlightCreate(FlightBase):
    pass


class FlightUpdate(BaseModel):
    destination: str | None = Field(default=None, min_length=2, max_length=100)
    price: Decimal | None = Field(default=None, gt=0)
    flight_class: Literal["economy", "business"] | None = None
    has_seats: bool | None = None


class FlightResponse(FlightBase):
    id: int


class BookingCreate(BaseModel):
    flight_id: int
    passenger_id: int
    # Regex валідація номера місця: ряд 1-99 та літера від A до F (наприклад: 12A, 1B, 24F)
    seat_number: str = Field(..., pattern=r"^\d{1,2}[A-F]$")


class BookingResponse(BaseModel):
    id: int
    flight_id: int
    passenger_id: int
    booking_reference: str
    seat_number: str
    status: str