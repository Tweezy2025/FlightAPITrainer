from api_tester.backend.app.models.booking import BookingCreateSingle


def test_booking_model():
    model = BookingCreateSingle(
        flight_number="SU100",
        passenger="Test",
        email="321321@example.com",
        phone="+79990001122",
        has_luggage=True
    )

    assert model.flight_number == "SU100"
    assert model.has_luggage is True
