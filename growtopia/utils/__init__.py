# isort:skip_file
from logging import (
    DEBUG as LOG_LEVEL_DEBUG,
    INFO as LOG_LEVEL_INFO,
    WARNING as LOG_LEVEL_WARNING,
    ERROR as LOG_LEVEL_ERROR,
    CRITICAL as LOG_LEVEL_CRITICAL,
)

from .buffer import *
from .compression import *
from .crypto import *
from .setup import *

logger = Setup.setup_logger("growtopia")


def log(level: int, msg: str) -> None:
    logger.log(level, msg)
