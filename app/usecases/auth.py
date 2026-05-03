from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UserRepository


class AuthUseCase:
    """
    Бизнес-логика аутентификации
    """
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def register(self, email: str, password: str) -> User:
        """
        Регистрирует нового пользователя
        """
        existing = await self._user_repo.get_by_email(email)
        if existing:
            raise ConflictError("User with this email already exists")

        hashed = hash_password(password)
        user = User(email=email, password_hash=hashed)
        return await self._user_repo.create(user)

    async def login(self, email: str, password: str) -> dict:
        """
        Аутентифицирует пользователя и возвращает JWT-токен
        """
        user = await self._user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")

        token = create_access_token(
            sub=str(user.id),
            role=str(user.role),
        )
        return {"access_token": token, "token_type": "bearer"}

    async def get_profile(self, user_id: int) -> User:
        """
        Возвращает профиль пользователя по ID
        """
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
