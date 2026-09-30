from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description="Personalized workout and nutrition guidance powered by Gemini AI.",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": "FitBuddy",
    }