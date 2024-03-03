__all__ = (
    "Logger",
    "Log",
    "LogLevel",
    "log",
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
from typing import List, Union

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

    _queue: List[Union[Log, AnsiStr]] = []

    _disabled: bool = False

    running: bool = False

    @classmethod
    def start(cls) -> bool:
        if cls._disabled:
            return False

        if cls.running and cls._thread:
            cls.running = False
            cls._thread.join()

        cls.running = True

        cls._thread = Thread(target=cls.log_loop, daemon=True)
        cls._thread.start()

        return True

    @classmethod
    def stop(cls) -> None:
        cls.running = False

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
        while cls.running:
            cls._queue_event.wait()

            queue: List[Log]

            with cls._queue_lock:
                queue = cls._queue.copy()
                cls._queue.clear()

            for message in queue:
                print(message)

            with cls._wait_cond:
                cls._wait_cond.notify_all()

            cls._queue_event.clear()

    @classmethod
    def wait_until_flushed(cls) -> None:
        if cls._disabled:
            return

        with cls._queue_lock:
            if not cls._queue:
                return

        with cls._wait_cond:
            cls._wait_cond.wait()


def log(log_level: LogLevel, message: str) -> None:
    Logger.log(message, log_level)


def disable_logger() -> None:
    Logger.stop()
    Logger._disabled = True
