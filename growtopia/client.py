__all__ = ("Client",)

import asyncio

import enet

from .context import Context
from .dispatcher import Dispatcher
from .enums import EventID
from .host import Host
from .protocol import GameMessagePacket, HelloPacket, Packet, PacketType, TextPacket


class Client(Host, Dispatcher):
    """
    Represents a Growtopia game client. This class uses the Host class as base and extends its functionality.
    This class can also be used as a base class for other types of clients (e.g proxy client (redirects packets to server)).

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
        Host.__init__(
            self,
            None,
            kwargs.get("peer_count", 1),
            kwargs.get("channel_limit", 2),
            kwargs.get("incoming_bandwidth", 0),
            kwargs.get("outgoing_bandwidth", 0),
        )
        Dispatcher.__init__(self)

        self.compress_with_range_coder()
        self.checksum = enet.ENET_CRC32

        self.__address: tuple[str, int] = address
        self.__peer: enet.Peer = None
        self.__running: bool = False

    def connect(self) -> enet.Peer:
        """
        Connects to the server.

        Returns
        -------
        enet.Peer
            The peer that was used to connect to the server.
        """
        self.__peer = super().connect(enet.Address(*self.__address), 2, 0)
        return self.__peer

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
        if self.__peer is None:
            return

        if send_quit:
            packet = GameMessagePacket()
            packet.game_message = "action|quit\n"

            self.send(packet=packet)

        self.__peer.disconnect_now(0)
        self.__peer = None

    def send(self, packet: Packet = None, data: bytes = None) -> None:
        if data is not None:
            packet = Packet(data)

        if self.__peer is not None:
            self.__peer.send(0, packet.enet_packet)

    def start(self) -> None:
        """
        Starts the server.

        Returns
        -------
        None
        """
        self.__running = True
        asyncio.run(self.run())

    def stop(self) -> None:
        """
        Stops the server.

        Returns
        -------
        None
        """
        self.__running = False

    async def run(self) -> None:
        """
        Starts the asynchronous loop that handles events accordingly.

        Returns
        -------
        None
        """

        if self.__peer is None:
            self.connect()

        self.__running = True

        while self.__running:
            event = self.service(0, True)

            if event is None:
                await asyncio.sleep(0)
                continue

            context = Context()
            context.client = self
            context.enet_event = event

            if event.type == enet.EVENT_TYPE_CONNECT:
                await self.dispatch_event(EventID.ON_CONNECT, context)
                continue

            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                await self.dispatch_event(EventID.ON_DISCONNECT, context)
                continue

            elif event.type == enet.EVENT_TYPE_RECEIVE:
                if (type_ := Packet.get_type(event.packet.data)) == PacketType.HELLO:
                    context.packet = HelloPacket(event.packet.data)
                elif type_ == PacketType.TEXT:
                    context.packet = TextPacket(event.packet.data)
                elif type_ == PacketType.GAME_MESSAGE:
                    context.packet = GameMessagePacket(event.packet.data)

                if not await self.dispatch_event(
                    context.packet.identify() if context.packet else EventID.ON_RECEIVE,
                    context,
                ):
                    await self.dispatch_event(EventID.ON_UNHANDLED, context)

        await self.dispatch_event(
            EventID.ON_CLEANUP,
            context,
        )
