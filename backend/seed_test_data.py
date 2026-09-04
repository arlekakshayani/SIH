from datetime import date
from app.database import SessionLocal, engine, Base
from app.models.flight import FlightPrice
from app.models.index import AirfareIndex

# Ensure tables exist locally
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Add a mock flight observation batch for today
sample_routes = [("DEL-BOM", 5400.0), ("BLR-DEL", 4800.0), ("HYD-MAA", 3700.0)]
for route, base in sample_routes:
    for window in [1, 7, 15, 30]:
        multiplier = 1.8 if window == 1 else (1.2 if window == 7 else 1.0)
        fare = base * multiplier
        db.add(FlightPrice(
            route=route,
            airline="IndiGo",
            flight_number="6E-101",
            departure_date=date.today(),
            departure_time="10:00",
            arrival_time="12:15",
            booking_date=date.today(),
            advance_days=window,
            cabin_class="Economy",
            base_fare=fare - 600,
            taxes=600.0,
            total_fare=fare,
            source="seed_script"
        ))

db.commit()
db.close()
print("Test flight observations seeded successfully!")
