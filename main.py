from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.starlette import register_tortoise

from app.settings.db import DATABASE



def get_app() -> FastAPI:
    app = FastAPI()
    
    # Routes
    
    # Fixtures
    
    # Dev only
    
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