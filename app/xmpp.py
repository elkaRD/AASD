import asyncio
import time
import uuid
from typing import Optional

import aioxmpp
from aioxmpp import JID


class ServerUnavailableError(RuntimeError):
    pass


class XMPPServer:
    def __init__(self, domain: str) -> None:
        super().__init__()
        self._jid = aioxmpp.JID(None, domain, None)

    @property
    def domain(self) -> str:
        return self._jid.domain

    @property
    def jid(self) -> aioxmpp.JID:
        return self._jid

    async def async_is_available(
        self, loop: Optional[asyncio.BaseEventLoop] = None, timeout: float = 60
    ) -> bool:
        try:
            await aioxmpp.node.connect_xmlstream(
                self.jid,
                aioxmpp.make_security_layer(None, no_verify=True),
                negotiation_timeout=timeout,
                loop=loop,
            )
            return True
        except aioxmpp.errors.MultiOSError:
            return False

    def is_available(self, timeout: float = 60) -> bool:
        return asyncio.run(self.async_is_available(timeout=timeout))

    def wait_until_available(
        self, tries: int = 5, delay: float = 1, backoff: float = 2, timeout: float = 60
    ) -> None:
        t_tries, t_delay = tries, delay
        while t_tries > 0:
            if self.is_available(timeout):
                return
            time.sleep(t_delay)
            t_tries -= 1
            t_delay *= backoff
        raise ServerUnavailableError(f"Server not available after {tries} tries")


class JIDGenerator:
    def __init__(self, domain: str) -> None:
        self.domain = domain

    def generate(self) -> JID:
        return JID.fromstr(f"{uuid.uuid4().hex}@{self.domain}")
