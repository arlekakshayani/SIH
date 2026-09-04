# System Architecture

## Component Separation
1. **Data Collection Layer (`scraper/`)**: Captures flight fare observations and formats them according to our Data Contract.
2. **API & Persistence Layer (`backend/`)**: Validates data via Pydantic, stores it in PostgreSQL via SQLAlchemy, and serves REST endpoints.
3. **Econometric Engine (`backend/app/services/`)**: Computes elementary Jevons geometric mean indices and upper-level Laspeyres aggregations.
4. **Presentation Layer (`frontend/`)**: Renders yield curves, time-series charts, and MoSPI export tools.
