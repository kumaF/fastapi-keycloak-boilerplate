from fastapi import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi.param_functions import Depends

from ..services import UserService
from ..models import (
    User,
    UpdateUser
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth/token")


@router.post('')
async def sign_up(user: User):
    service = UserService()
    return await service.create_new_user(user)


@router.get('/me')
async def current_user(token: str = Depends(oauth2_scheme)):
    service = UserService()
    return await service.get_current_user(token)


@router.patch('')
async def update_user(user: UpdateUser, token: str = Depends(oauth2_scheme)):
    service = UserService()
    return await service.update_user(user, token)


# @router.delete('')
# async def delete_user(token: str = Depends(oauth2_scheme)):
#     service = UserService()
#     return await service.delete_user(token)
