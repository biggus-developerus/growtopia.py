__all__ = ("Server",)

import asyncio
from abc import ABC, abstractmethod

import enet

from ..context import ServerContext
from ..dispatcher import Dispatcher
from ..enums import EventID
from .server_player_pool import ServerPlayerPool


class Server(enet.Host, Dispatcher, ServerPlayerPool, ABC):
    """
    Represents a server. This class uses the enet.Host class as a base class and extends its functionality.
    This class is also used as a base class for other types of servers, such as GameServer and LoginServer.

    Parameters
    ----------
    address: tuple[str, int]
        The address to bind the server to.

    Kwarg Parameters
    ----------------
    peer_count: int
        The maximum amount of peers that can connect to the server.
    channel_limit: int
        The maximum amount of channels that can be used.
    incoming_bandwidth: int
        The maximum incoming bandwidth.
    outgoing_bandwidth: int
        The maximum outgoing bandwidth.

    Attributes
    ----------
    running: bool
        Whether the server is running or not.
    """

    def __init__(
        self,
        address: tuple[str, int],
        **kwargs,
    ) -> None:
        enet.Host.__init__(
            self,
            enet.Address(*address),
            kwargs.get("peer_count", 32),
            kwargs.get("channel_limit", 2),
            kwargs.get("incoming_bandwidth", 0),
            kwargs.get("outgoing_bandwidth", 0),
        )
        Dispatcher.__init__(self)
        ServerPlayerPool.__init__(self)

        self.compress_with_range_coder()
        self.checksum = enet.ENET_CRC32

        self.running: bool = False

    def start(self) -> None:
        """
        Starts the server.

        Returns
        -------
        None
        """
        self.running = True
        asyncio.run(self.run())

    def stop(self) -> None:
        """
        Stops the server.

        Returns
        -------
        None
        """
        self.running = False

    async def run(self) -> None:
        """
        Starts the asynchronous loop that handles events accordingly.

        Returns
        -------
        None
        """
        self.running = True
        await self.dispatch_event(EventID.ON_READY, self)

        while self.running:
            event = self.service(0, True)

            if event is None:
                await asyncio.sleep(0)
                continue

            context = ServerContext()
            context.server = self
            context.enet_event = event

            res = await self._handle_event(context)

            if not res:
                await self.dispatch_event(
                    EventID.ON_UNHANDLED, context
                )  # dispatch the ON_UNHANDLED event if the packet isn't handled by the user but recognised by growtopia.py

        await self.dispatch_event(
            EventID.ON_CLEANUP,
            self,
        )

    @abstractmethod
    async def _handle_event(self, context: ServerContext) -> None:
        ...
