"""Configures application logging using loguru."""

import sys
from loguru import logger


def setup_logger() -> None:
    """Configures loguru for application-wide logging."""

    # Remove default handler
    logger.remove()

    # Add custom handler
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    logger.info("Logger configured successfully")