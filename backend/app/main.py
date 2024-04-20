# generated by fastapi-codegen:
#   filename:  api.swagger.yaml
#   timestamp: 2024-04-18T23:37:43+00:00

from __future__ import annotations

from fastapi import FastAPI

from app.routers import auth, activities

app = FastAPI(
    title='InnoTrackify API',
    description='API used for our application InnoTrackify.',
    version='0.1.0',
    servers=[{'url': 'http://localhost:8000/api', 'description': 'local server'}],
)

app.include_router(auth.router)
app.include_router(activities.router)


@app.get("/")
async def root():
    return {"message": "Gateway of the App"}