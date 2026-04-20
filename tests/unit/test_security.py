from api_tester.backend.app.core.security import hash_password, verify_password


def test_password_hashing():
    pwd = "secret123"
    hashed = hash_password(pwd)

    assert hashed != pwd
    assert verify_password(pwd, hashed)
