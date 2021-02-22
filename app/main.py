import uvicorn

from starlette.middleware.cors import CORSMiddleware
from fastapi import (
    FastAPI,
    HTTPException
)

from .exceptions import http_exception_handler
from .configs import API_PREFIX
from .utils import (
    startup_handler,
    shutdown_handler
)

from .routes import (
    HealthRoutes,
    UserRoutes,
    AuthRoutes
)


app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)

app.include_router(HealthRoutes, prefix=f'{API_PREFIX}/health')
app.include_router(UserRoutes, prefix=f'{API_PREFIX}/users')
app.include_router(AuthRoutes, prefix=f'{API_PREFIX}/oauth')

app.add_exception_handler(HTTPException, http_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
