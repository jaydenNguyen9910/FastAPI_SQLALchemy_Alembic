from fastapi import APIRouter

from app.api.endpoints import test
from app.api.endpoints.fastapi_users import fastapi_users, bearer_jwt_backend, cookie_jwt_backend, google_oauth_client
from app.core.settings import settings
from app.schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter()

router.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["registration"])
router.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["verification"])
router.include_router(fastapi_users.get_auth_router(bearer_jwt_backend, requires_verification=True),
                      prefix="/auth/bearer_jwt", tags=["login/logout"])
router.include_router(fastapi_users.get_auth_router(cookie_jwt_backend, requires_verification=True),
                      prefix="/auth/cookie_jwt", tags=["login/logout"])
router.include_router(fastapi_users.get_oauth_router(google_oauth_client, cookie_jwt_backend, settings.JWT_SECRET,
                                                     associate_by_email=True), prefix="/auth/google", tags=["oauth2"])
router.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["password management"])
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
                      prefix="/users", tags=["users management"])
router.include_router(test.router, prefix="", tags=["test"])
