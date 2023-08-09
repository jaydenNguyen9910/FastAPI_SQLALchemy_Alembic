import uuid
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, CookieTransport, JWTStrategy
from httpx_oauth.clients.google import GoogleOAuth2

from app.db.database import User
from app.services.fastapi_users import get_user_manager
from app.core.settings import settings

# Transports
bearer_transport = BearerTransport(tokenUrl="auth/bearer_jwt/login")
cookie_transport = CookieTransport(cookie_max_age=3600)


# Strategies
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=3600)


# Backends
bearer_jwt_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

cookie_jwt_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [cookie_jwt_backend, bearer_jwt_backend],
)

current_active_user = fastapi_users.current_user(active=True)

google_oauth_client = GoogleOAuth2("588085546511-o14noi1q0qgbssji7240t35ared5hqf2.apps.googleusercontent.com",
                                   "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")
