from tests.utils.helpers import assert_json_list


def test_get_all_flights(auth_client):
    response = auth_client.get("/api/flights/")
    assert response.status_code == 200

    data = assert_json_list(response)
    assert len(data) > 0

    for flight in data:
        assert "flight_number" in flight
        assert "departure" in flight
        assert "arrival" in flight
        assert "price" in flight
        assert "seats_available" in flight


def test_filter_flights_by_departure(auth_client):
    response = auth_client.get("/api/flights/?departure=SVO")
    assert response.status_code == 200

    data = assert_json_list(response)
    for flight in data:
        assert flight["departure"] == "SVO"


def test_filter_flights_by_departure_and_arrival(auth_client):
    response = auth_client.get("/api/flights/?departure=SVO&arrival=LED")
    assert response.status_code == 200

    data = assert_json_list(response)
    for flight in data:
        assert flight["departure"] == "SVO"
        assert flight["arrival"] == "LED"


def test_filter_flights_by_date(auth_client):
    response = auth_client.get("/api/flights/")
    assert response.status_code == 200

    flights = assert_json_list(response)
    assert len(flights) > 0

    departure_time = flights[0]["departure_time"]
    date_only = departure_time.split("T")[0]

    response = auth_client.get(f"/api/flights/?date={date_only}")
    assert response.status_code == 200

    filtered = assert_json_list(response)
    assert len(filtered) > 0

    for flight in filtered:
        assert flight["departure_time"].startswith(date_only)
