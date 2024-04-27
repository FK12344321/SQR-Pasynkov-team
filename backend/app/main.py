from __future__ import annotations

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.routers import auth, activities
from app.models import Error, IncorrectUser, IncorrectToken


app = FastAPI(
    title='InnoTrackify API',
    description='API used for our application InnoTrackify.',
    version='0.1.0',
    servers=[{'url': 'http://localhost:8000/api',
              'description': 'local server'},
             {'url': 'http://10.90.137.146/:8000/api'}],
)

app.include_router(auth.router)
app.include_router(activities.router)


@app.get("/")
async def root():
    return {"message": "Gateway of the App"}


@app.exception_handler(IncorrectUser)
async def incorrect_user_exception_handler():
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=Error(
            message='Incorrect username or password',
            description='Try to change your username or password',
        ).model_dump(mode='json')
    )


@app.exception_handler(IncorrectToken)
async def incorrect_token_exception_handler(exc: IncorrectUser):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=Error(
            message=f'Incorrect authorization {exc.token_type} token',
            description='Your token must be taken from login() or refresh_token() methods',
        ).model_dump(mode='json')
    )


@app.exception_handler(Exception)
async def internal_error_handler():
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=Error(
            message='Something went wrong',
            description='Internal Server Error, something went wrong',
        ).model_dump(mode='json')
    )
