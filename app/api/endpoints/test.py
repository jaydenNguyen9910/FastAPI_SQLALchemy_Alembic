from fastapi import APIRouter, Depends

from app.api.endpoints.fastapi_users import current_active_user
from app.db.database import User

router = APIRouter()


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
