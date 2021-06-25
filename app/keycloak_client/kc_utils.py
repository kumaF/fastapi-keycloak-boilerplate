import logging

from keycloak import (
    KeycloakAdmin,
    KeycloakOpenID
)

from ..configs import (
    KEYCLOAK_SERVER,
    KEYCLOAK_REALM,
    KEYCLOAK_CLIENT,
    KEYCLOAK_PASSWORD,
    KEYCLOAK_USERNAME,
    SECRET_KEY
)


class KeycloakClient:
    admin: KeycloakAdmin = None
    openid: KeycloakOpenID = None


kc = KeycloakClient()

def init_kc_admin():
    logging.info('Initializing keycloak admin client...')
    try:
        kc.admin = KeycloakAdmin(
            server_url=KEYCLOAK_SERVER,
            username=KEYCLOAK_USERNAME,
            password=KEYCLOAK_PASSWORD,
            realm_name='master',
            verify=True,
            auto_refresh_token=['get', 'put', 'post', 'delete']
        )

        logging.info('Initialized keycloak admin client')
    except:
        logging.error('Failed initializing keycloak admin client')

def init_openid():
    logging.info('Initializing openid client...')
    try:
        kc.openid = KeycloakOpenID(
            server_url=KEYCLOAK_SERVER,
            client_id=KEYCLOAK_CLIENT,
            realm_name=KEYCLOAK_REALM,
            client_secret_key=SECRET_KEY
        )

        logging.info('Initialized openid client')
    except:
        logging.error('Failed initializing openid client')


def get_clients():
    return kc.admin, kc.openid