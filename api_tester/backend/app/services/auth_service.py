from api_tester.backend.app.db.mongo import db
from api_tester.backend.app.models.user import UserCreate, UserInDB
from api_tester.backend.app.core.security import verify_password, hash_password, create_access_token


class AuthService:

    @staticmethod
    def register_user(data: UserCreate):
        existing = db.users.find_one({"username": data.username})
        if existing:
            raise ValueError("User already exists")

        hashed = hash_password(data.password)

        user = {
            "username": data.username,
            "hashed_password": hashed
        }

        db.users.insert_one(user)
        return {"status": "registered"}

    @staticmethod
    def authenticate_user(username: str, password: str):
        user = db.users.find_one({"username": username})
        if not user:
            raise ValueError("Invalid username or password")

        if not verify_password(password, user["hashed_password"]):
            raise ValueError("Invalid username or password")

        token = create_access_token({"sub": username})
        return {"access_token": token, "token_type": "bearer"}
