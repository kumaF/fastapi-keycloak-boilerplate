import os
from typing import cast

from starlette.config import Config

config = Config('.env')

API_VERSION = config('API_VERSION', cast=str, default='v0.1')
API_PREFIX = f'/api/{API_VERSION}'

MONGO_HOST = config('MONGO_HOST', cast=str, default='127.0.0.1')
MONGO_PORT = config('MONGO_PORT', cast=str, default='27017')
MONGO_DB_NAME = config('MONGO_DB_NAME', cast=str, default='sample_app_auth')
MONGO_USERNAME = config('MONGO_USERNAME', cast=str, default='admin')
MONGO_PASSWORD = config('MONGO_PASSWORD', cast=str, default='password')

MONGO_USERS_COLLECTION = config("MONGO_USERS_COLLECTION", cast=str, default='users_collection')

# MONGO_URL = f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}'
MONGO_URL = f'mongodb://{MONGO_HOST}:{MONGO_PORT}'
MONGO_TIMEOUT = 1000

SECRET_KEY = config('SECRET_KEY', cast=str, default='fc463eb5-d6f8-4f37-971b-6261407fec5d')
ALGORITHM = config('ALGORITHM', cast=str, default='HS256')
ACCESS_TOKEN_EXP = config('ACCESS_TOKEN_EXP', cast=int, default=60*24)
REFRESH_TOKEN_EXP = config('REFRESH_TOKEN_EXP', cast=int, default=60*24*30)


KEYCLOAK_SERVER = config('KEYCLOAK_SERVER', cast=str, default='http://localhost:8080/auth/')
KEYCLOAK_USERNAME = config('KEYCLOAK_USERNAME', cast=str, default='admin')
KEYCLOAK_PASSWORD = config('KEYCLOAK_PASSWORD', cast=str, default='password')
KEYCLOAK_REALM = config('KEYCLOAK_REALM', cast=str, default='myrealm')
KEYCLOAK_CLIENT = config('KEYCLOAK_CLIENT', cast=str, default='myclient')
