from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """
    Запрос на регистрацию
    """
    email: EmailStr
    password: str = Field(...,
        min_length=8,
        max_length=16,
        description="Пароль пользователя, 8-16 символов",
    )


class TokenResponse(BaseModel):
    """
    Ответ с JWT токеном
    """
    access_token: str
    token_type: str = "bearer"
