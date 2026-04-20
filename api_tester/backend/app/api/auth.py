from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api_tester.backend.app.models.user import UserCreate
from api_tester.backend.app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])


@router.post("/register")
def register_user(data: UserCreate):
    try:
        return AuthService.register_user(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        return AuthService.authenticate_user(
            username=form_data.username,
            password=form_data.password
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
