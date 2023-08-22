__all__ = ("Client",)

import asyncio
from abc import ABC, abstractmethod

from ..context import ClientContext
from ..dispatcher import Dispatcher
from ..enums import EventID
from .client_net import ClientNet


class Client(ClientNet, Dispatcher, ABC):
    """
    Represents a client.
    This class can also be used as a base class for other types of clients (e.g game client, proxy client (redirects packets to server)).

    Parameters
    ----------
    address: tuple[str, int]
        The address of the server to connect to.

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
    """

    def __init__(self, address: tuple[str, int], **kwargs) -> None:
        ClientNet.__init__(self, address, **kwargs)
        Dispatcher.__init__(self)

        self.running: bool = False

    def start(self) -> None:
        """
        Starts the server.

        Returns
        -------
        None
        """
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
        if self._peer is None:
            self.connect()

        self.running = True
        await self.dispatch_event(EventID.ON_READY, self)

        while self.running:
            event = self._host.service(0, True)

            if event is None:
                await asyncio.sleep(0)
                continue

            context = ClientContext()
            context.client = self
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
    async def _handle_event(self, context: ClientContext) -> None:
        ...
