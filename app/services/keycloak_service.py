import json
from keycloak.exceptions import KeycloakError
from fastapi import HTTPException

from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_503_SERVICE_UNAVAILABLE
)

from keycloak import (
    KeycloakAdmin,
    KeycloakOpenID
)

from ..keycloak_client import get_clients
from ..models import UpdateUser
from ..configs import (
    KEYCLOAK_SERVER,
    KEYCLOAK_USERNAME,
    KEYCLOAK_PASSWORD,
    KEYCLOAK_REALM,
    KEYCLOAK_CLIENT,
    SECRET_KEY
)

class KeyCloakService:
    def __init__(self) -> None:
        super().__init__()
        self._keycloak_admin, self._keycloak_openid = get_clients()

    async def create_user(self, user: dict):
        self._keycloak_admin.realm_name = KEYCLOAK_REALM
        payload: dict = {
            'email': user.get('email'),
            'username': user.get('username'),
            'firstName': user.get('first_name'),
            'lastName': user.get('last_name'),
            'credentials': [{'value': user.get('password'), 'type': 'password'}],
            'realmRoles': ['user_default', ],
            'enabled': True
        }

        try:
            return self._keycloak_admin.create_user(payload)
        except KeycloakError as e:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail=json.loads(e.error_message)['errorMessage']
            )

    async def update_user(self, user: UpdateUser, user_id: str):
        self._keycloak_admin.realm_name = KEYCLOAK_REALM
        payload: dict = {}

        if bool(user.email):
            payload.update({'email': user.email})
        
        if bool(user.first_name):
            payload.update({'firstName': user.first_name})

        if bool(user.last_name):
            payload.update({'lastName': user.last_name})

        if bool(user.password):
            payload.update({'credentials': [{'value': user.password, 'type': 'password'}]})

        try:
            return self._keycloak_admin.update_user(user_id=user_id, payload=payload)
        except KeycloakError as e:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail=json.loads(e.error_message)['errorMessage']
            )

    async def generate_tokens(self, username: str, password: str):
        try:
            return self._keycloak_openid.token(
                username=username,
                password=password
            )
        except KeycloakError as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=json.loads(e.error_message)['error_description']
            )
    
    async def refresh_tokens(self, refresh_token: str):
        try:
            return self._keycloak_openid.refresh_token(refresh_token)
        except KeycloakError as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=json.loads(e.error_message)['error_description']
            )

    async def validate_token(self, access_token: str):
        try:
            public_key: str = f'-----BEGIN PUBLIC KEY-----\n{self._keycloak_openid.public_key()}\n-----END PUBLIC KEY-----'
            options: dict = {
                'verify_signature': True, 
                'verify_aud': True,
                'verify_exp': True
            }

            user_info: dict = self._keycloak_openid.userinfo(token=access_token)
            token_info: dict = self._keycloak_openid.decode_token(
                token=access_token,
                key=public_key,
                options=options
            )

            return {
                'token_info': token_info,
                'user_info': user_info
            }

        except Exception as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='Token has expired'
            )

