from fastapi import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi.param_functions import Depends, Body

from ..services import AuthService
from ..models import LoginUser


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth/token")


@router.post('/token')
async def login(user: LoginUser = Body(None, embed=True), grant_type: str = Body(...), refresh_token: str = Body(None)):
    service = AuthService()
    return await service.generate_access_token(user, grant_type, refresh_token)


@router.get('/auth')
async def authenticate(token: str = Depends(oauth2_scheme)):
    service = AuthService()
    return await service.validate_token(token)
