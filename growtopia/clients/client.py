__all__ = ("Client",)

import asyncio
from abc import ABC, abstractmethod
from typing import Union

import enet

from ..context import ClientContext
from ..dispatcher import Dispatcher
from ..enums import EventID
from ..protocol import (
    GameMessagePacket,
    GameUpdatePacket,
    HelloPacket,
    StrPacket,
    TextPacket,
)


class Client(Dispatcher, ABC):
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
        self._host = enet.Host(
            None,
            kwargs.get("peer_count", 1),
            kwargs.get("channel_limit", 2),
            kwargs.get("incoming_bandwidth", 0),
            kwargs.get("outgoing_bandwidth", 0),
        )
        Dispatcher.__init__(self)

        self._host.compress_with_range_coder()
        self._host.checksum = enet.ENET_CRC32

        self.running: bool = False

        self._address: tuple[str, int] = address
        self._peer: enet.Peer = None

    def connect(self) -> enet.Peer:
        """
        Connects to the server.

        Returns
        -------
        enet.Peer
            The peer that was used to connect to the server.
        """
        self._peer = self._host.connect(enet.Address(*self._address), 2, 0)
        return self._peer

    def disconnect(self, send_quit: bool = True) -> None:
        """
        Disconnects from the server.

        Parameters
        ----------
        send_quit: bool
            Whether to send the quit packet to the server.

        Returns
        -------
        None
        """
        if self._peer is None:
            return

        if send_quit:
            self.send(packet=TextPacket("action|quit_to_exit\n"))
            self.send(packet=GameMessagePacket("action|quit\n"))

            self.running = False

        self._peer.disconnect_now(0)
        self._peer = None

    def send(self, packet: Union[StrPacket, GameUpdatePacket, HelloPacket]) -> bool:
        """
        Sends a packet to the host.

        Parameters
        ----------
        packet: Union[StrPacket, GameUpdatePacket, HelloPacket]
            The packet to send to the host.

        Returns
        -------
        bool:
            True if the packet was successfully sent, False otherwise.
        """
        if self._peer is not None:
            return True if self._peer.send(0, packet.enet_packet) == 0 else False

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
            context,
        )

    @abstractmethod
    async def _handle_event(self, context: ClientContext) -> None:
        ...
