# API Documentation

## Run the backend

From the repository root:

```powershell
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger at `http://127.0.0.1:8000/docs`.

The backend uses PostgreSQL when `DATABASE_URL` is configured and falls back to
the local `backend/airfare_db.db` SQLite database for development.

## Planned & Active Endpoints

### Ingestion & Raw Data
- `GET /`: Health check and system status.
- `POST /api/flights/batch`: Submit normalized flight observation batch.
- `GET /api/flights/`: Flight pricing observations. Supports `route`, `advance_days`, and `limit`.
- `GET /api/routes/`: Distinct tracked flight corridors.

### Index Metrics
- `POST /api/index/calculate`: Trigger daily index computation.
- `GET /api/index/latest`: Fetch recent index figures.
- `GET /api/index/history`: Historical index time-series metrics.

### Export
- `GET /api/export/csv`: MoSPI-compliant eSankhyiki CSV data export.

## Sample responses

### `POST /api/flights/batch`

```json
{
	"status": "success",
	"records_received": 1,
	"records_saved": 1
}
```

### `GET /api/index/latest`

```json
[
	{
		"id": 1,
		"date": "2026-09-05",
		"route": "COMPOSITE",
		"index_value": 108.42,
		"base_value": 100.0,
		"calculation_method": "Jevons_Advance_Weighted",
		"sample_size": 24,
		"created_at": "2026-09-05T12:00:00Z"
	}
]
```

### `GET /api/routes/`

```json
["DEL-BOM", "BLR-DEL", "HYD-MAA"]
```

Invalid route filters or invalid flight payloads return HTTP `422`. Database
failures return HTTP `503` with a JSON `detail` message.
