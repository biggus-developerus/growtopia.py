__all__ = ("Setup",)

import logging

LOG_LEVEL_COLORS = {
    "DEBUG": "\033[90m",  # "GRAY
    "INFO": "\033[94m",  # "BLUE"
    "WARNING": "\033[93m",  # "YELLOW"
    "ERROR": "\033[91m",  # "RED"
    "CRITICAL": "\033[91m" + "\033[1m" + "\033[4m",  # "RED" + "BOLD" + "UNDERLINE"
}

ANSI_RESET = "\033[0m"


class ColouredFrmtr(logging.Formatter):
    def format(self, record):
        colour = LOG_LEVEL_COLORS.get(record.levelname, "")
        msg = super().format(record)
        lvl_name = record.levelname
        return f"{colour}{record.name.upper()} - [{lvl_name}] {msg}{ANSI_RESET}"


class Setup:
    @staticmethod
    def setup_logger(name: str, min_level: int = logging.INFO) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(min_level)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            ColouredFrmtr(fmt="%(asctime)s - %(message)s", datefmt="%H:%M:%S")
        )

        logger.addHandler(stream_handler)

        return logger
