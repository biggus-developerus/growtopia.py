__all__ = ("Host",)

import asyncio
import time
from typing import Optional

import enet

from .event import Event


class Host(enet.Host):
    """
    Represents an enet.Host object. This classes uses the enet.Host class as a base class and extends its functionality.

    Parameters
    ----------
    address: enet.Address
        The address to bind the host to.
    peer_count: int
        The maximum amount of peers that can connect to the host.
    channel_limit: int
        The maximum amount of channels that can be used.
    incoming_bandwidth: int
        The maximum incoming bandwidth.
    outgoing_bandwidth: int
        The maximum outgoing bandwidth.

    Attributes
    ----------
    None (enet.Host)
    """

    def __init__(
        self,
        address: enet.Address,
        peer_count: int,
        channel_limit: int,
        incoming_bandwidth: int,
        outgoing_bandwidth: int,
    ) -> None:
        super().__init__(
            address,
            peer_count,
            channel_limit,
            incoming_bandwidth,
            outgoing_bandwidth,
        )

        self.__running: bool = False

    def start(self) -> None:
        """
        Runs the coroutine that starts the asynchronous loop.

        Returns
        -------
        None
        """
        asyncio.run(self.run())

    def stop(self) -> None:
        """
        Stops the running asynchronous loop and dispatches the on_cleanup event.

        Returns
        -------
        None
        """

        self.__running = False
        self._handle(Event(None))

    async def run(self) -> None:
        """
        Starts an asynchronous loop that handles events accordingly.

        Returns
        -------
        None
        """
        self.__running = True
        while self.__running:
            event = self.service(0, True)

            if event:
                if await self._handle((ev := Event(event))):
                    ev.handled = True
                continue

            await asyncio.sleep(0)

    async def _handle(self, event: Optional[Event]) -> None:
        """
        Handles event data accordingly.

        Parameters
        ----------
        event: Optional[Event]
            The event to dispatch.

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            If this method is not overridden. (e.g not implemented in a subclass)
        """
        raise NotImplementedError
