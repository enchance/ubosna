from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.starlette import register_tortoise

from app.settings.db import DATABASE
from app.routes import devrouter, authrouter
from app.auth import fusers


def get_app() -> FastAPI:
    app = FastAPI()     # noqa
    
    # Routes: Main
    app.include_router(authrouter, prefix='/auth', tags=['Authentication'])
    # app.include_router(fusers.get_register_router(), prefix='/auth', tags=['Authentication'])
    
    # Routes: Fixtures
    
    # Routes: Dev
    app.include_router(devrouter, prefix='/dev', tags=['Development'])
    
    # Tortoise
    register_tortoise(app, config=DATABASE, generate_schemas=True)
    
    # CORS
    origins = ['http://localhost:3000', 'https://localhost:3000']   # For React
    app.add_middleware(
        CORSMiddleware, allow_origins=origins, allow_credentials=True,
        allow_methods=["*"], allow_headers=["*"],
    )
    
    return app



app = get_app()