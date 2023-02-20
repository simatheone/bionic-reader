from sqlalchemy import update

from app.db.db import get_async_session
from app.models import User


async def update_user_is_verified_field(user_email: str) -> None:
    async for session in get_async_session():
        await session.execute(
            update(User).
            where(User.email == user_email).
            values(is_verified=True)
        )
        await session.commit()
