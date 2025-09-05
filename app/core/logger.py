"""Configures application logging using loguru."""

import sys
from loguru import logger


def setup_logger(log_level: str = "INFO") -> None:
    """Configures loguru for application-wide logging."""

    # Remove default handler
    logger.remove()

    # Add custom handler with configurable level
    logger.add(
        sys.stdout,
        level=log_level.upper(),
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    logger.info(f"Logger configured successfully with level: {log_level.upper()}")