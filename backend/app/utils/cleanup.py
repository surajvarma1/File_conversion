"""Background cleanup tasks for temporary files."""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any

from app.core.logging import get_logger

logger = get_logger(__name__)


async def periodic_cleanup(storage: Any, ttl_seconds: int, interval_seconds: int, stop_event: asyncio.Event):
    """Periodically clean up old temporary files.

    Args:
        storage: Storage instance with `cleanup_old_files(ttl_seconds)` method.
        ttl_seconds: Time-to-live for files.
        interval_seconds: How often to run the cleanup.
        stop_event: Asyncio event to stop the loop.
    """
    logger.info("Starting periodic cleanup task")
    try:
        while not stop_event.is_set():
            try:
                deleted = await storage.cleanup_old_files(ttl_seconds)
                logger.info(f"Cleanup run complete, deleted {deleted} files")
            except Exception as e:
                logger.error(f"Cleanup task encountered an error: {str(e)}")

            await asyncio.wait_for(stop_event.wait(), timeout=interval_seconds)
    except asyncio.TimeoutError:
        # Timeout expired, loop continues
        pass
    except asyncio.CancelledError:
        logger.info("Cleanup task cancelled")
    finally:
        logger.info("Periodic cleanup task stopped")
