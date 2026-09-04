# Automated Airfare Price Index System (MoSPI)

An automated platform for collecting domestic airfares across Indian routes to compute real-time price indices (Jevons / Laspeyres models), designed to support Consumer Price Index (CPI) inflation tracking for the Ministry of Statistics and Programme Implementation (MoSPI).

## Architecture Overview
- **Scraper**: Collects flight observations from authorized feeds/APIs or calibrated mock engine across 1d, 7d, 15d, 30d advance booking windows.
- **Backend**: FastAPI, SQLAlchemy 2.x, Pydantic, PostgreSQL.
- **Processing**: Pandas and NumPy for Jevons geometric mean and DGCA weighted Laspeyres index compilation.
- **Frontend**: React dashboard (planned) for visual analytics.

## Structure
- `backend/`: Server-side API and database persistence.
- `scraper/`: Data collection and normalizer scripts.
- `frontend/`: React user interface dashboard.
- `docs/`: Technical specifications and database documentation.
- `data/`: Local raw and processed snapshots.