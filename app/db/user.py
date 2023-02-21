from typing import Union, Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers,
                           InvalidPasswordException, UUIDIDMixin)
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_async_session
from app.db.settings import settings
from app.models import User
from app.schemas.user import UserCreate
from app.services.email import send_email
from .user_update import update_user_is_verified_field


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason='Password should be at least 8 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        receiver_email = user.email
        await update_user_is_verified_field(receiver_email)
        message = (
            'Subject: Welcome to Bionic Reader\n\n'
            f'Hello {user.first_name}!\n\n'
            'Great to have you with us.\n'
            'This is the e-mail address you registered on '
            'bionic-reader.app:\n'
            'Use it to log in or recover your password, not that you\'d'
            ' ever forget.\n\n'
            'Best wishes,\n'
            'The Bionic Reader Team'
        ).encode('utf-8')
        await send_email(receiver_email, message)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        reset_password_link = (
            settings.ALLOW_ORIGINS + '/reset-password?token=' + token
        )
        message = (
            'Subject: Password reset link\n\n'
            f'Hello {user.first_name}!\n\n'
            'You have indicated that you forgot your password. Please click on'
            ' the link below to reset your password:\n'
            f'{reset_password_link}\n\n'
            'If you did not ask to change your password, then you can ignore'
            ' this email and your password will not be changed.\n\n'
            'Best wishes,\n'
            'The Bionic Reader Team'
        ).encode('utf-8')
        receiver_email = user.email
        await send_email(receiver_email, message)

    async def on_after_reset_password(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        message = (
            'Subject: Your New Password Is Set\n\n'
            'Success!\n'
            'Your new password is in place and ready to use.\n'
            'If you didn’t change your password, we recommend that you reset'
            ' it now to make sure your account stays secure.\n\n'
            'Best wishes,\n'
            'The Bionic Reader Team'
        ).encode('utf-8')
        receiver_email = user.email
        await send_email(receiver_email, message)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


cookie_transport = CookieTransport(
    cookie_max_age=settings.COOKIE_MAX_AGE,
    cookie_name=settings.COOKIE_NAME,
    cookie_secure=settings.COOKIE_SECURE,
    cookie_httponly=settings.COOKIE_HTTPONLY,
    cookie_samesite=settings.COOKIE_SAMESITE,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET,
        lifetime_seconds=settings.LIFETIME_SECONDS
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
