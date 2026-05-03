import time

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Превращает пароль в хэш
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля хэшу
    """
    return pwd_context.verify(password, hashed_password)


def _now() -> int:
    """
    Вспомогательная функция, выдающая текущее время
    """
    return int(time.time())


def create_access_token(sub: str, role: str) -> str:
    """
    Создаёт закодированный JWT токен
    """
    payload = {
        "sub": sub,
        "role": role,
        "iat": _now(),
        "exp": _now() + settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(token: str) -> dict:
    """
    Декодирует и проверяет JWT токен
    """
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
