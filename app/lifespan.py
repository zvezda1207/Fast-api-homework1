from contextlib import asynccontextmanager
from fastapi import FastAPI
from .models import init_orm, close_orm, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('START LIFESPAN')
    await init_orm()  
    yield  
    await close_orm()
    print('FINISH LIFESPAN')

async def close_orm():
    print("Closing ORM...")
    await engine.dispose()
    print("ORM Closed.")