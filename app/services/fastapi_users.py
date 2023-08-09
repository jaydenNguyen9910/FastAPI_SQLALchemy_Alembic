import logging
import uuid
from typing import Optional, Union, Dict, Any
from fastapi import Depends, Request
from fastapi.openapi.models import Response
from fastapi_users import BaseUserManager, UUIDIDMixin, InvalidPasswordException

from app.core.settings import settings
from app.db.database import get_user_db, User
from app.schemas.user import UserCreate
from app.utils.send_email import send_email, USER_VERIFICATION_TEMPLATE

logger = logging.getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.JWT_SECRET
    verification_token_secret = settings.JWT_SECRET

    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_update(
            self,
            user: User,
            update_dict: Dict[str, Any],
            request: Optional[Request] = None,
    ):
        logger.info(f"User {user.id} has been updated with {update_dict}.")

    async def on_after_login(
            self,
            user: User,
            request: Optional[Request] = None,
            response: Optional[Response] = None,
    ):
        logger.info(f"User {user.id} logged in.")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"Verification requested for user {user.id}. Verification token: {token}")
        await send_email(to=user.email,
                         subject="[EXAMPLE] Verification code for user authentication",
                         template=USER_VERIFICATION_TEMPLATE,
                         title="Verification code for user authentication",
                         verification_code=token)

    async def on_after_verify(
            self, user: User, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has been verified")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")
        await send_email(to=user.email,
                         subject="[EXAMPLE] Verification code for user to reset password",
                         template=USER_VERIFICATION_TEMPLATE,
                         title="Verification code for user to reset password",
                         verification_code=token)

    async def on_after_reset_password(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has reset their password.")

    async def on_before_delete(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} is going to be deleted")

    async def on_after_delete(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} is successfully deleted")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
