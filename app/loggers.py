from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def log(self, msg: str) -> None:
        pass


class NullLogger(Logger):
    def log(self, msg: str) -> None:
        pass


class ConsoleLogger(Logger):
    def log(self, msg: str) -> None:
        print(msg)
