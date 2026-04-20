from api_tester.backend.app.db.mongo import db
from tests.utils.helpers import auth_client


def test_get_airlines(auth_client):
    airlines = list(db.airlines.find({}))
    assert len(airlines) > 0

    response = auth_client.get("/api/airlines/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(airlines)

    db_names = {a["name"] for a in airlines}
    api_names = {a["name"] for a in data}

    assert db_names == api_names
