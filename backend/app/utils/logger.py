from pathlib import Path

from loguru import logger

from app.config.settings import settings


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

logger.add(
    LOG_DIR / "app.log",
    rotation="10 MB",
    retention="10 days",
    level=settings.LOG_LEVEL,
    enqueue=True,
)

logger.add(
    sink=lambda msg: print(msg, end=""),
    level=settings.LOG_LEVEL,
)

__all__ = ["logger"]