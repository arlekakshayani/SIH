from typing import List
from sqlalchemy.orm import Session
from app.models.flight import FlightPrice
from app.schemas.flight import FlightCreateSchema

class FlightCleaningService:
    """
    Business logic for cleaning, deduplicating, and persisting flight records.
    """

    @staticmethod
    def clean_and_save_batch(db: Session, flight_items: List[FlightCreateSchema]) -> int:
        """
        Takes a list of validated flight records from Pydantic,
        checks for duplicate observations on the same flight and date,
        and saves unique records to PostgreSQL.
        """
        saved_count = 0

        for item in flight_items:
            # Query if this specific flight observation already exists
            existing_record = db.query(FlightPrice).filter(
                FlightPrice.flight_number == item.flight_number.strip().upper(),
                FlightPrice.departure_date == item.departure_date,
                FlightPrice.booking_date == item.booking_date,
                FlightPrice.advance_days == item.advance_days
            ).first()

            if not existing_record:
                # Convert the Pydantic schema to an ORM database model
                flight_record = FlightPrice(
                    route=item.route.strip().upper(),
                    airline=item.airline.strip(),
                    flight_number=item.flight_number.strip().upper(),
                    departure_date=item.departure_date,
                    departure_time=item.departure_time,
                    arrival_time=item.arrival_time,
                    booking_date=item.booking_date,
                    advance_days=item.advance_days,
                    cabin_class=item.cabin_class,
                    base_fare=item.base_fare,
                    taxes=item.taxes,
                    total_fare=item.total_fare,
                    source=item.source
                )
                db.add(flight_record)
                saved_count += 1

        # Commit transaction to PostgreSQL
        db.commit()
        return saved_count
