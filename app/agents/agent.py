from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterator, Optional, Union

from aioxmpp import JID
from spade import agent as sa, behaviour as sb

from loggers import Logger, NullLogger


class WithLogging:
    @abstractmethod
    def get_logger(self) -> Logger:
        pass

    def log_prefix(self) -> str:
        return type(self).__qualname__

    def log(self, msg: str) -> None:
        self.get_logger().log(f"{self.log_prefix()}: {msg}")


class WithJIDLogging(WithLogging, ABC):
    @abstractmethod
    def get_jid(self) -> JID:
        pass

    def log_prefix(self) -> str:
        return f"{super().log_prefix()} ({self.get_jid()})"


class CyclicBehaviour(sb.CyclicBehaviour, WithJIDLogging, ABC):
    def __init__(self, jid: JID, logger: Logger = NullLogger()):
        super().__init__()
        self._jid = jid
        self._logger = logger

    def get_jid(self) -> JID:
        return self._jid

    def get_logger(self) -> Logger:
        return self._logger


class OneShotBehaviour(sb.OneShotBehaviour, WithJIDLogging, ABC):
    def __init__(self, jid: JID, logger: Logger = NullLogger()):
        super().__init__()
        self._jid = jid
        self._logger = logger

    def get_jid(self) -> JID:
        return self._jid

    def get_logger(self) -> Logger:
        return self._logger


class PeriodicBehaviour(sb.PeriodicBehaviour, WithJIDLogging, ABC):
    def __init__(
            self,
            jid: JID,
            period: float,
            logger: Logger = NullLogger(),
            start_at: Optional[datetime] = None
    ):
        super().__init__(period, start_at)
        self._jid = jid
        self._logger = logger

    def get_jid(self) -> JID:
        return self._jid

    def get_logger(self) -> Logger:
        return self._logger


class TimeoutBehaviour(sb.TimeoutBehaviour, WithJIDLogging, ABC):
    def __init__(
            self,
            jid: JID,
            start_at: datetime,
            logger: Logger = NullLogger()
    ):
        super().__init__(start_at)
        self._jid = jid
        self._logger = logger

    def get_jid(self) -> JID:
        return self._jid

    def get_logger(self) -> Logger:
        return self._logger


class State(sb.State, WithJIDLogging, ABC):
    def __init__(self, jid: JID, logger: Logger = NullLogger()):
        super().__init__()
        self._jid = jid
        self._logger = logger

    def get_jid(self) -> JID:
        return self._jid

    def get_logger(self) -> Logger:
        return self._logger


class FSMBehaviour(sb.FSMBehaviour, WithJIDLogging, ABC):
    def __init__(self, jid: JID, logger: Logger = NullLogger()):
        super().__init__()
        self._jid = jid
        self._logger = logger

    def get_jid(self) -> JID:
        return self._jid

    def get_logger(self) -> Logger:
        return self._logger


Behaviour = sb.CyclicBehaviour


class Agent(sa.Agent, WithJIDLogging, ABC):
    def __init__(
            self,
            jid: Union[str, JID],
            password: str,
            logger: Logger = NullLogger()
    ):
        super().__init__(str(jid), password)
        self._logger = logger

    def get_jid(self) -> JID:
        return self.jid

    def get_logger(self) -> Logger:
        return self._logger

    @abstractmethod
    def get_behaviours(self) -> Iterator[Behaviour]:
        pass

    async def setup(self) -> None:
        self.log(f"Starting")
        for behaviour in self.get_behaviours():
            self.add_behaviour(behaviour)
