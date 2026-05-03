from app.core.config import settings
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    """
    Бизнес-логика работы с LLM
    """
    def __init__(
        self,
        chat_repo: ChatMessageRepository,
        openrouter_client: OpenRouterClient,
    ) -> None:
        self._chat_repo = chat_repo
        self._openrouter = openrouter_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
        temperature: float = 0.7,
        model: str | None = None,
    ) -> str:
        """
        Обрабатывает запрос пользователя к LLM и возвращает ответ
        """
        
        messages: list[dict] = []
        if system:
            messages.append({"role": "system", "content": system})

        if max_history > 0:
            history = await self._chat_repo.get_recent_messages(user_id, max_history)
            for msg in history:
                messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": prompt})

        await self._chat_repo.add_message(user_id, role="user", content=prompt)

        answer = await self._openrouter.chat_completion(
            messages=messages,
            model=model or settings.OPENROUTER_MODEL,
            temperature=temperature,
        )

        await self._chat_repo.add_message(user_id, role="assistant", content=answer)

        return answer
    
    async def get_history(self, user_id: int, limit: int = 10) -> list[dict]:
        """
        Возвращает последние сообщения пользователя
        """
        messages = await self._chat_repo.get_recent_messages(user_id, limit)
        return [{"role": m.role, "content": m.content} for m in messages]

    async def clear_history(self, user_id: int) -> None:
        """
        Удаляет всю историю сообщений пользователя
        """
        await self._chat_repo.delete_all_by_user(user_id)
