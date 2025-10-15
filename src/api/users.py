from fastapi import APIRouter, Depends, Request, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.upload_file import UploadFileService
from src.services.users import UserService
from src.database.db import get_db
from src.conf.config import settings
from src.schemas import User
from src.services.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/me", response_model=User, description="No more than 5 requests per minute"
)
@limiter.limit("5/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    return user


@router.patch("/avatar", response_model=User)
async def update_avatar_user(
    file: UploadFile = File(),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    avatar_url = UploadFileService(
        settings.CLOUDINARY_NAME,
        settings.CLOUDINARY_API_KEY,
        settings.CLOUDINARY_API_SECRET,
    ).upload_file(file, user.username)

    user_service = UserService(db)
    user = await user_service.update_avatar_url(user.email, avatar_url)

    return user
