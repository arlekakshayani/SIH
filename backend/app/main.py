from fastapi import FastAPI
from app.database import engine, Base
import app.models.flight  # Ensures FlightPrice model is registered
import app.models.index   # Ensures AirfareIndex model is registered
from app.routes import flights, routes, index, export

# 1. Automatically create all physical database tables if they do not exist
Base.metadata.create_all(bind=engine)

# 2. Instantiate FastAPI App
app = FastAPI(
    title="Automated Airfare Price Index System (MoSPI)",
    description="Real-Time Airfare Price Index for Domestic Flight Routes",
    version="1.0.0"
)

# 3. Include Routers
app.include_router(flights.router)
app.include_router(routes.router)
app.include_router(index.router)
app.include_router(export.router)

@app.get("/")
def root_health_check():
    return {
        "status": "online",
        "system": "MoSPI Domestic Airfare Price Index Backend",
        "modules": ["ingestion", "index_engine", "export"]
    }
