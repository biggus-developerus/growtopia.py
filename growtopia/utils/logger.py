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
from threading import (
    Condition,
    Event,
    Lock,
    Thread,
)
from time import sleep
from typing import Union

from ..constants import (
    LOG_LOOP_SLEEP_TIME,
)
from .ansi import (
    AnsiESC,
    AnsiStr,
)


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
            AnsiESC(self._log_level.value)
        )


class Logger:
    _thread: Union[Thread, None] = None

    _wait_cond: Condition = Condition()
    _queue_event: Event = Event()
    _queue_lock: Lock = Lock()

    _queue: list[Union[Log, AnsiStr]] = []

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
    def stop(cls) -> None:
        cls._running = False

        if cls._thread:
            cls._thread.join()
            cls._thread = None

    @classmethod
    def log(cls, message: str, log_level: LogLevel = LogLevel.INFO) -> None:
        with cls._queue_lock:
            cls._queue.append(Log(log_level, message))

        cls._queue_event.set()

    @classmethod
    def log_ansi(cls, message: AnsiStr) -> None:
        with cls._queue_lock:
            cls._queue.append(message)

        cls._queue_event.set()

    @classmethod
    def log_loop(cls) -> None:
        while cls._running:
            cls._queue_event.wait()

            queue = []

            with cls._queue_lock:
                queue = cls._queue.copy()
                cls._queue.clear()

            for message in queue:
                print(message)

            with cls._wait_cond:
                cls._wait_cond.notify_all()

            cls._queue_event.clear()

            sleep(LOG_LOOP_SLEEP_TIME)

    @classmethod
    def wait_until_flushed(cls) -> None:
        while True:
            with cls._wait_cond:
                cls._wait_cond.wait()
                # wait until the queue is empty
                # we break immediately after because the condition
                # is only notified when the queue is empty
                break


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
