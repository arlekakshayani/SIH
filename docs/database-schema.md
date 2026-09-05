# Database Schema Design

## Primary Tables

### `flight_prices`
Stores micro-level flight quotations captured over time.
- `id` (Integer, Primary Key)
- `route` (String, e.g., "DEL-BOM")
- `airline` (String, e.g., "IndiGo")
- `flight_number` (String, e.g., "6E-2054")
- `departure_date` (Date)
- `departure_time` (String)
- `arrival_time` (String)
- `booking_date` (Date)
- `advance_days` (Integer: 1, 7, 15, 30)
- `cabin_class` (String)
- `base_fare` (Float)
- `taxes` (Float)
- `total_fare` (Float)
- `source` (String)
- `scraped_at` (DateTime)

### `airfare_index`
Stores aggregated, precomputed index values over time.
- `id` (Integer, Primary Key)
- `date` (Date)
- `route` (String, e.g., "DEL-BOM" or "COMPOSITE")
- `index_value` (Float)
- `base_value` (Float)
- `calculation_method` (String)
- `sample_size` (Integer)
- `created_at` (DateTime)
