from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

async def http_exception_handler(request: Request, e: HTTPException):
    return JSONResponse(
        status_code = e.status_code,
        content = {
            "success": False,
            "detail": e.detail
        },
    )

def grequest_exception_handler(request, exception):
    raise HTTPException(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f'grequest {exception}'
    )
