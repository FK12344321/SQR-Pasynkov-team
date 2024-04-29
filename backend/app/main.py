from __future__ import annotations

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.routers import auth, activities
from app.models import Error, IncorrectUser, IncorrectToken

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


app = FastAPI(
    title='InnoTrackify API',
    description='API used for our application InnoTrackify.',
    version='0.1.0',
    servers=[{'url': 'http://localhost:8000/api',
              'description': 'local server'},
             {'url': 'http://10.90.137.146:8000'}],
)
limiter = Limiter(get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.state.limiter = limiter

Instrumentator().instrument(app).expose(app)

app.include_router(auth.router)
app.include_router(activities.router)


@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request, response: Response):
    return {"message": "Gateway of the App"}


@app.exception_handler(IncorrectUser)
async def incorrect_user_exception_handler(*args, **kwargs):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=Error(
            message='Incorrect username or password',
            description='Try to change your username or password',
        ).model_dump(mode='json')
    )


@app.exception_handler(IncorrectToken)
async def incorrect_token_exception_handler(r: Request, exc: IncorrectUser):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=Error(
            message=f'Incorrect authorization {exc.token_type} token',
            description='Your token must be taken from login() or refresh_token() methods',  # noqa: E501
        ).model_dump(mode='json')
    )


@app.exception_handler(Exception)
async def internal_error_handler(*args, **kwargs):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=Error(
            message='Something went wrong',
            description='Internal Server Error, something went wrong',
        ).model_dump(mode='json')
    )
