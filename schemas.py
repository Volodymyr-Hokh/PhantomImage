from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    telegram_id: int


class UserInDB(User):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
