from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    """
    Публичная модель пользователя
    """
    id: int
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)
