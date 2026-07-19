'''Configuring logging for the entire project'''

import logging
from pathlib import Path

import boto3

from src.config import (
    AWS_REGION,
    CLOUDWATCH_ENABLED,
    CLOUDWATCH_LOG_GROUP,
    CLOUDWATCH_LOG_STREAM,
)

# Create logs directory if it doesn't exist
LOG_FOLDER = Path("logs")
LOG_FOLDER.mkdir(exist_ok=True)

LOG_FILE = LOG_FOLDER / "opspulse.log"


def get_logger(name: str):

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # CloudWatch Handler (optional - never breaks local/CI runs if disabled or misconfigured)
    if CLOUDWATCH_ENABLED:
        try:
            import watchtower

            cloudwatch_client = boto3.client("logs", region_name=AWS_REGION)

            cloudwatch_handler = watchtower.CloudWatchLogHandler(
                log_group=CLOUDWATCH_LOG_GROUP,
                stream_name=CLOUDWATCH_LOG_STREAM,
                boto3_client=cloudwatch_client,
            )
            cloudwatch_handler.setFormatter(formatter)
            logger.addHandler(cloudwatch_handler)

        except Exception as e:
            logger.warning(f"CloudWatch logging unavailable: {e}")

    return logger