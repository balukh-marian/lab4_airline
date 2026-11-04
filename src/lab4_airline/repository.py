import random
from typing import Any

from .database import get_db_connection
from .models import BookingCreate, FlightCreate, FlightUpdate


class AirlineRepository:
    """Репозиторій для роботи з сутностями рейсів та бронювань."""

    def get_flights(
        self, destination: str | None = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        query = "SELECT * FROM flights"
        params: list[Any] = []

        if destination:
            query += " WHERE destination ILIKE %s"
            params.append(f"%{destination}%")

        query += " ORDER BY id LIMIT %s"
        params.append(limit)

        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(query, tuple(params))
            return cur.fetchall()

    def get_flight_by_id(self, flight_id: int) -> dict[str, Any] | None:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM flights WHERE id = %s", (flight_id,))
            return cur.fetchone()

    def create_flight(self, flight: FlightCreate) -> dict[str, Any]:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO flights (flight_number, destination, departure_date, price, flight_class, has_seats)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    flight.flight_number,
                    flight.destination,
                    flight.departure_date,
                    flight.price,
                    flight.flight_class,
                    flight.has_seats,
                ),
            )
            return cur.fetchone()

    def update_flight(
        self, flight_id: int, flight: FlightUpdate
    ) -> dict[str, Any] | None:
        update_data = {k: v for k, v in flight.model_dump().items() if v is not None}
        if not update_data:
            return self.get_flight_by_id(flight_id)

        set_clause = ", ".join(f"{key} = %s" for key in update_data)
        values = list(update_data.values())
        values.append(flight_id)

        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(
                f"UPDATE flights SET {set_clause} WHERE id = %s RETURNING *",
                tuple(values),
            )
            return cur.fetchone()

    def delete_flight(self, flight_id: int) -> bool:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "DELETE FROM flights WHERE id = %s RETURNING id", (flight_id,)
            )
            return cur.fetchone() is not None

    def create_booking(self, booking: BookingCreate) -> dict[str, Any]:
        booking_ref = f"BK-{random.randint(2000, 9999)}"
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO bookings (flight_id, passenger_id, booking_reference, seat_number, status)
                VALUES (%s, %s, %s, %s, 'CONFIRMED')
                RETURNING *
                """,
                (
                    booking.flight_id,
                    booking.passenger_id,
                    booking_ref,
                    booking.seat_number,
                ),
            )
            return cur.fetchone()

    def get_bookings(self, limit: int = 50) -> list[dict[str, Any]]:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM bookings ORDER BY id DESC LIMIT %s", (limit,)
            )
            return cur.fetchall()