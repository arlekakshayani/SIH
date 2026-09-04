# API Documentation

## Planned & Active Endpoints

### Ingestion & Raw Data
- `GET /`: Health check and system status.
- `POST /api/flights/batch`: Submit normalized flight observation batch.
- `GET /api/flights`: Paginated flight pricing observations.
- `GET /api/routes`: Distinct tracked flight corridors.

### Index Metrics
- `POST /api/index/calculate`: Trigger daily index computation.
- `GET /api/index/latest`: Fetch recent index figures.
- `GET /api/index/history`: Historical index time-series metrics.

### Export
- `GET /api/export/csv`: MoSPI-compliant eSankhyiki CSV data export.
