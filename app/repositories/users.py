from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UserRepository:
    """
    Репозиторий для работы с таблицей пользователей
    """
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        """
        Возвращает пользователя по email или None, если нет
        """
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        """
        Возвращает пользователя по ID или None, если нет
        """
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """
        Сохраняет нового пользователя в базу данных
        """
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
