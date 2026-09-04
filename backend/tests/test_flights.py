from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_flight_and_route_read_apis():
    flights_response = client.get("/api/flights/?limit=1")
    routes_response = client.get("/api/routes/")

    assert flights_response.status_code == 200
    assert isinstance(flights_response.json(), list)
    assert routes_response.status_code == 200
    assert isinstance(routes_response.json(), list)


def test_invalid_route_filter_is_rejected():
    response = client.get("/api/flights/?route=invalid-route")

    assert response.status_code == 422


def test_frontend_origin_is_allowed_by_cors():
    response = client.options(
        "/api/routes/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_index_history_and_export_apis():
    latest_response = client.get("/api/index/latest")
    history_response = client.get("/api/index/history?limit=10")
    export_response = client.get("/api/export/csv")

    assert latest_response.status_code == 200
    assert isinstance(latest_response.json(), list)
    assert history_response.status_code == 200
    assert isinstance(history_response.json(), list)
    assert export_response.status_code == 200
    assert export_response.headers["content-type"].startswith("text/csv")


def test_invalid_flight_batch_is_rejected_before_database_write():
    response = client.post("/api/flights/batch", json=[{"route": "not-a-route"}])

    assert response.status_code == 422
