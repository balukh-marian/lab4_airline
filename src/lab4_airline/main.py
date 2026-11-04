import psycopg
from fastapi import FastAPI, HTTPException, status

from .models import (
    BookingCreate,
    BookingResponse,
    FlightCreate,
    FlightResponse,
    FlightUpdate,
)
from .repository import AirlineRepository

app = FastAPI(
    title="Airline Booking API",
    description="REST API для управління авіарейсами та бронюванням квитків",
    version="1.0.0",
)

repo = AirlineRepository()


@app.get(
    "/flights", response_model=list[FlightResponse], summary="Отримати список рейсів"
)
def read_flights(destination: str | None = None, limit: int = 50):
    return repo.get_flights(destination=destination, limit=limit)


@app.get(
    "/flights/{flight_id}",
    response_model=FlightResponse,
    summary="Отримати рейс за ID",
)
def read_flight(flight_id: int):
    flight = repo.get_flight_by_id(flight_id)
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Рейс не знайдено"
        )
    return flight


@app.post(
    "/flights",
    response_model=FlightResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Створити новий рейс",
)
def create_flight(flight: FlightCreate):
    try:
        return repo.create_flight(flight)
    except psycopg.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@app.put(
    "/flights/{flight_id}",
    response_model=FlightResponse,
    summary="Оновити дані рейсу",
)
def update_flight(flight_id: int, flight: FlightUpdate):
    updated = repo.update_flight(flight_id, flight)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Рейс не знайдено"
        )
    return updated


@app.delete(
    "/flights/{flight_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити рейс",
)
def delete_flight(flight_id: int):
    success = repo.delete_flight(flight_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Рейс не знайдено"
        )


@app.post(
    "/bookings",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Створити бронювання квитка",
)
def create_booking(booking: BookingCreate):
    try:
        return repo.create_booking(booking)
    except psycopg.Error as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@app.get(
    "/bookings",
    response_model=list[BookingResponse],
    summary="Отримати список бронювань",
)
def read_bookings(limit: int = 50):
    return repo.get_bookings(limit=limit)