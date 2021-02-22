from fastapi import HTTPException
from fastapi.param_functions import Body
from starlette.status import (
    HTTP_200_OK, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)

from ..utils import build_response

from ..db import (
    get_client,
    MongoDB
)

from ..models import (
    LoginUser,
    OutUser
)

from ..services import (
    KeyCloakService
)


class AuthService:
    def __init__(self):
        super().__init__()
        self._db = MongoDB(get_client())
        self._keycloak_service = KeyCloakService()

    async def generate_access_token(self, login_user: LoginUser = Body(None, embed=True), grant_type: str = Body(...), refresh_token: str = Body(None)):
        if grant_type == 'password' and login_user is not None:
            login_user: dict = login_user.dict()

            username: str = login_user['username']
            password: str = login_user['password']

            if not bool(username) and bool(login_user.get('email', None)):
                user_dict: dict = await self._db.get_user(login_user['email'])

                if not bool(user_dict):
                    raise HTTPException(
                        status_code=HTTP_400_BAD_REQUEST,
                        detail='Invalid email address',
                        headers={'Authenticate': 'Bearer'}
                    )

                username = user_dict['username']

            response = await self._keycloak_service.generate_tokens(username, password)
            return await build_response(data=response)

        if grant_type == 'refresh_token' and refresh_token is not None:
            response = await self._keycloak_service.refresh_tokens(refresh_token)
            return await build_response(status_code=HTTP_200_OK, data=response)

        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid grant type or token',
            headers={'Authenticate': 'Bearer'}
        )

    async def validate_token(self, token: str):
        response = await self.check_active_token(token)
        return await build_response(status_code=HTTP_200_OK, data=response)

    async def check_active_token(self, token: str):
        response: dict = await self._keycloak_service.validate_token(token)
        user_dict: dict = await self._db.get_user_by_id(response.get('user_info').get('sub'))

        if bool(user_dict):
            user_dict.update({'meta': response})
            return user_dict

        raise HTTPException(
            status_code=HTTP_204_NO_CONTENT,
            detail='Not a valid user token',
        )
