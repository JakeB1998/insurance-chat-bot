import logging
import os


def load_from_file(fp, logger = None):

    if logger is None:
        logger = logging.getLogger(__name__)

    try:
        with open(fp, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        logger.error(f"Failed to load context from {fp}", e)