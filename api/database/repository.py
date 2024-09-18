from sqlalchemy.future import select

from api.database.models import User, session


async def add_user(
    telegram_id: int, username: str, first_name: str, last_name: str
) -> User:
    async with session() as s:
        async with s.begin():
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            s.add(user)
            return user


async def get_user_by_telegram_id(telegram_id: int) -> User:
    async with session() as s:
        async with s.begin():
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await s.execute(stmt)
            user = result.scalar()
            return user
