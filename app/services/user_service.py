from fastapi import HTTPException
from starlette.responses import JSONResponse
from iteration_utilities import unique_everseen

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)

from ..services import (
    KeyCloakService,
    AuthService
)

from ..utils import build_response

from ..db import (
    MongoDB,
    get_client
)

from ..models.user_models import (
    OutUser,
    User,
    MongoUser,
    UpdateUser
)


class UserService:
    def __init__(self):
        super().__init__()
        self._db = MongoDB(get_client())
        self._keycloak_service = KeyCloakService()
        self._auth_service = AuthService()

    async def create_new_user(self, user: User):
        user_dict: dict = user.dict()
        user_id: str = await self._keycloak_service.create_user(user_dict)
        user_dict.update({'user_id': user_id})
        user_dict.pop('password')

        _ = await self._db.insert_user(MongoUser(**user_dict).dict())

        return await build_response(HTTP_201_CREATED, msg='New user created')

    async def get_current_user(self, token: str):
        user_dict: dict = await self._auth_service.check_active_token(token)
        return await build_response(data=OutUser(**user_dict).dict())

    async def update_user(self, user: UpdateUser, token: str):
        current_data: dict = await self._auth_service.check_active_token(token)
        _ = await self._keycloak_service.update_user(user, current_data.get('user_id'))

        update_user: dict = user.dict(exclude_unset=True)

        updated_user = await self._db.update_user(update_user, current_data.get('user_id'))
        return await build_response(data=OutUser(**updated_user).dict())

    # async def delete_user(self, token: str):
    #     user_dict: dict = await self._auth_service.check_active_token(token)
    #     user = await self._db.delete_user(user_dict['email'])

    #     if user:
    #         return await build_response(msg='Removed user successfully')

    #     raise HTTPException(
    #         status_code=HTTP_204_NO_CONTENT,
    #         detail='Remove user failed'
    #     )
