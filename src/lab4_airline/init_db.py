import random
from datetime import date, timedelta

import psycopg

DSN = "postgresql://postgres:postgres@localhost:5432/airline_db"

DDL_STATEMENTS = """
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS passengers CASCADE;
DROP TABLE IF EXISTS flights CASCADE;

CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    flight_number VARCHAR(10) UNIQUE NOT NULL,
    destination VARCHAR(100) NOT NULL,
    departure_date DATE NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    flight_class VARCHAR(20) NOT NULL,
    has_seats BOOLEAN DEFAULT TRUE
);

CREATE TABLE passengers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    passport_number VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    flight_id INT NOT NULL REFERENCES flights(id) ON DELETE CASCADE,
    passenger_id INT NOT NULL REFERENCES passengers(id) ON DELETE CASCADE,
    booking_reference VARCHAR(20) UNIQUE NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    status VARCHAR(20) DEFAULT 'CONFIRMED'
);
"""

DESTINATIONS = [
    "London",
    "Paris",
    "Warsaw",
    "Berlin",
    "Rome",
    "Madrid",
    "Vienna",
    "Prague",
]
CLASSES = ["economy", "business"]
FIRST_NAMES = [
    "Ivan",
    "Petro",
    "Anna",
    "Olena",
    "Maksym",
    "Yuliia",
    "Danylo",
    "Sofiia",
    "Oleh",
    "Viktoriia",
]
LAST_NAMES = [
    "Tkachenko",
    "Melnyk",
    "Boyko",
    "Koval",
    "Shevchenko",
    "Kovalchuk",
    "Bondar",
]


def init_database() -> None:
    with psycopg.connect(DSN) as conn, conn.cursor() as cur:
        cur.execute(DDL_STATEMENTS)

        for i in range(1, 16):
            flight_num = f"LH-{100 + i}"
            dest = random.choice(DESTINATIONS)
            dep_date = date.today() + timedelta(days=random.randint(1, 30))
            price = round(random.uniform(50.0, 300.0), 2)
            f_class = random.choice(CLASSES)
            cur.execute(
                """
                INSERT INTO flights (flight_number, destination, departure_date, price, flight_class, has_seats)
                VALUES (%s, %s, %s, %s, %s, TRUE);
                """,
                (flight_num, dest, dep_date, price, f_class),
            )

        for i in range(1, 21):
            name = (
                f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            )
            email = f"user_{i}_{random.randint(100, 999)}@gmail.com"
            passport = f"AA{random.randint(100000, 999999)}"
            cur.execute(
                """
                INSERT INTO passengers (full_name, email, passport_number)
                VALUES (%s, %s, %s);
                """,
                (name, email, passport),
            )

        for i in range(1, 26):
            flight_id = random.randint(1, 15)
            passenger_id = random.randint(1, 20)
            ref = f"BK-{random.randint(1000, 9999)}"
            seat = f"{random.randint(1, 30)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}"
            cur.execute(
                """
                INSERT INTO bookings (flight_id, passenger_id, booking_reference, seat_number, status)
                VALUES (%s, %s, %s, %s, 'CONFIRMED');
                """,
                (flight_id, passenger_id, ref, seat),
            )

        conn.commit()
        print("База даних успішно ініціалізована! Всього записів: 60")


if __name__ == "__main__":
    init_database()