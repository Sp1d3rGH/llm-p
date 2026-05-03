from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessageRepository:
    """
    Репозиторий для работы с сообщениями
    """
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """
        Сохраняет новое сообщение в базу данных
        """
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_recent_messages(self, user_id: int, limit: int) -> list[ChatMessage]:
        """
        Возвращает последние сообщения пользователя от старых к новым
        """
        subq = (
            select(ChatMessage.id)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
            .subquery()
        )
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.id.in_(select(subq)))
            .order_by(ChatMessage.created_at.asc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def delete_all_by_user(self, user_id: int) -> None:
        """
        Удаляет все сообщения пользователя
        """
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()
