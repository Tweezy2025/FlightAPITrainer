from api_tester.backend.app.db.mongo import db


def test_mongo_connection():
    assert db is not None
    assert isinstance(db.list_collection_names(), list)
