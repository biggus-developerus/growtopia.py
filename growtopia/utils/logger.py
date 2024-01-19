__all__ = (
    "Logger",
    "Log",
    "LogLevel",
    "log_info",
    "log_warning",
    "log_error",
    "log_critical",
    "disable_logger",
)

from datetime import datetime
from enum import Enum
from threading import Condition, Thread
from time import sleep
from typing import Union

from .ansi import AnsiESC, AnsiStr


class LogLevel(Enum):
    INFO = AnsiESC.BLUE
    WARNING = AnsiESC.YELLOW
    ERROR = AnsiESC.RED
    CRITICAL = AnsiESC.RED | AnsiESC.BOLD | AnsiESC.UNDERLINE


class Log:
    def __init__(self, log_level: LogLevel, message: str) -> None:
        self._log_level: LogLevel = log_level
        self._message: str = message
        self._time: str = datetime.now().strftime("%H:%M:%S")

    def __str__(self) -> AnsiStr:
        return AnsiStr(f"[{self._log_level.name}] {self._time} {self._message}").wrap(
            self._log_level.value
        )


class Logger:
    _instance: Union["Logger", None] = None
    _thread: Union[Thread, None] = None
    _condition: Condition = Condition()
    _queue: list[Log] = []
    _running: bool = False
    _disabled: bool = False

    @classmethod
    def start(cls) -> bool:
        if cls._disabled:
            return False

        if cls._running and cls._thread:
            cls._running = False
            cls._thread.join()

        cls._running = True

        cls._thread = Thread(target=cls.log_loop, daemon=True)
        cls._thread.start()

        return True

    @classmethod
    def stop(cls) -> bool:
        if not cls._running:
            return False

        cls._running = False

        cls._thread.join()
        cls._thread = None

        return True

    @classmethod
    def log(cls, message: str, log_level: LogLevel = LogLevel.INFO) -> None:
        with cls._condition:
            cls._queue.append(Log(log_level, message))
            cls._condition.notify()

    @classmethod
    def log_loop(cls) -> None:
        while cls._running:
            with cls._condition:
                cls._condition.wait()

                for message in cls._queue:
                    print(message)

                cls._queue.clear()

            sleep(0.1)  # try piling up some logs


def log_info(message: str) -> None:
    Logger.log(message, LogLevel.INFO)


def log_warning(message: str) -> None:
    Logger.log(message, LogLevel.WARNING)


def log_error(message: str) -> None:
    Logger.log(message, LogLevel.ERROR)


def log_critical(message: str) -> None:
    Logger.log(message, LogLevel.CRITICAL)


def disable_logger() -> None:
    Logger.stop()
    Logger._disabled = True
