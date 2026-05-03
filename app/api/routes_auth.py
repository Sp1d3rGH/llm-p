from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_usecase, get_current_user_id


router = APIRouter()


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    req: RegisterRequest,
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """
    Регистрация нового пользователя
    """
    try:
        user = await auth_usecase.register(email=req.email, password=req.password)
        return UserPublic.model_validate(user)
    except ConflictError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """
    Аутентификация пользователя
    """
    try:
        token_dict = await auth_usecase.login(
            email=form_data.username, password=form_data.password
        )
        return TokenResponse(**token_dict)
    except UnauthorizedError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/me", response_model=UserPublic)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """
    Возвращает профиль текущего пользователя
    """
    try:
        user = await auth_usecase.get_profile(user_id)
        return UserPublic.model_validate(user)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
