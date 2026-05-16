from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models
from app.routers.departments_router import router as department_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app started")

    yield

    print("app stopped")


app = FastAPI(lifespan=lifespan)

app.include_router(department_router)
