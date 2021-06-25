import json

from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_412_PRECONDITION_FAILED
)

from .keycloak_client import (
    init_openid,
    init_kc_admin
)

from .db import (
    open_db_connection,
    close_db_connection
)

async def validate_batch_responses(responses: list) -> list:
    resp: list = []

    for response in responses:
        if response.status_code in [200, 201]:
            data = json.loads(response.content.decode('utf-8'))
            resp.append(data.get('payload', data.get('detail', data)))
        elif response.status_code == 401:
            raise HTTPException(
                status_code=HTTP_412_PRECONDITION_FAILED,
                detail={
                    'reason': 'Authorize your account to contiue',
                    'url': response.url
                }
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail={
                    'reason': await inline_try_except('ref.json().get("detail", ref.reason)', 'ref.reason', response),
                    'url': response.url
                }
            )
    return resp


async def validate_response(response):
    if response.status_code in [200, 201]:
        data = response.json()
        return data.get('payload', data)
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail={
                'reason': await inline_try_except('ref.json().get("detail", ref.reason)', 'ref.reason', response),
                'url': response.url
            }
        )


async def build_response(status_code=HTTP_200_OK, **kwargs):
    payload = kwargs.get('data', None)
    detail = kwargs.get('msg', None)

    if bool(payload) and bool(detail):
        return JSONResponse(
            status_code=status_code,
            content={
                'success': True,
                'detail': detail,
                'payload': payload
            }
        )
    elif bool(payload):
        return JSONResponse(
            status_code=status_code,
            content={
                'success': True,
                'payload': payload
            }
        )
    elif bool(detail):
        return JSONResponse(
            status_code=status_code,
            content={
                'success': True,
                'detail': detail
            }
        )

async def inline_try_except(fn: str, default: str, ref):
    try:
        return eval(fn)
    except:
        return eval(default)


def startup_handler():
    init_kc_admin()
    init_openid()
    open_db_connection()

def shutdown_handler():
    close_db_connection()