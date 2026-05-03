from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.users import UserRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_chat_repo(db: AsyncSession = Depends(get_db)) -> ChatMessageRepository:
    return ChatMessageRepository(db)


def get_openrouter_client(request: Request) -> OpenRouterClient:
    client = request.app.state.openrouter_client
    return client


def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) -> AuthUseCase:
    return AuthUseCase(user_repo)


def get_chat_usecase(
    chat_repo: ChatMessageRepository = Depends(get_chat_repo),
    openrouter_client: OpenRouterClient = Depends(get_openrouter_client),
) -> ChatUseCase:
    return ChatUseCase(chat_repo, openrouter_client)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    Проверяет JWT токен и возвращает ID пользователя
    """
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    return user_id
