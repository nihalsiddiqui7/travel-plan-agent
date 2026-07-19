from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.database.session import engine
from app.utils.logger import logger
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")

    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar_one()

            logger.info(f"Database connected successfully! Result: {value}")

    except Exception as e:
        logger.exception(f"Database connection failed: {e}")
        raise

    yield

    logger.info("Shutting down application...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def home():
    logger.info("Home endpoint accessed")
    return {"message": f"Welcome to {settings.APP_NAME} version {settings.APP_VERSION}!"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}