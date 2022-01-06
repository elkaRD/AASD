import asyncio
import time
from numbers import Real
from typing import Optional

import aioxmpp
from aioxmpp.errors import MultiOSError


class ServerUnavailableError(RuntimeError):
    pass


class Server:
    def __init__(self, domain: str) -> None:
        super().__init__()
        self._jid = aioxmpp.JID.fromstr(domain)

    @property
    def domain(self) -> str:
        return self._jid.domain

    @property
    def jid(self) -> aioxmpp.JID:
        return self._jid

    async def async_is_available(
            self,
            loop: Optional[asyncio.BaseEventLoop] = None,
            timeout: Real = 60
    ) -> bool:
        try:
            await aioxmpp.node.connect_xmlstream(
                self.jid,
                aioxmpp.make_security_layer(None, no_verify=True),
                negotiation_timeout=timeout,
                loop=loop
            )
            return True
        except MultiOSError:
            return False

    def is_available(self, timeout: Real = 60) -> bool:
        return asyncio.run(self.async_is_available(timeout=timeout))

    def wait_until_available(
            self, tries: int = 5, delay: int = 1, backoff: int = 2
    ) -> None:
        t_tries, t_delay = tries, delay
        while t_tries > 0:
            print("X")
            if self.is_available():
                return
            time.sleep(t_delay)
            t_tries -= 1
            t_delay *= backoff
        raise ServerUnavailableError(
            f"Server not available after {tries} tries"
        )
