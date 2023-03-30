__all__ = ("Client",)

import asyncio

import enet

from .context import Context
from .enums import EventID
from .pool import Pool
from .protocol import Packet
from .utils import identify_packet


class Client(Pool):
    def __init__(self, address: tuple[str, int] = None, **kwargs) -> None:
        Pool.__init__(self)

        self.__address: tuple[str, int] = address
        self.__host: enet.Host = enet.Host(
            None,
            kwargs.get("max_peers", 1),
            kwargs.get("channels", 2),
            kwargs.get("in_bandwidth", 0),
            kwargs.get("out_bandwidth", 0),
        )

        self.__host.compress_with_range_coder()
        self.__host.checksum = enet.ENET_CRC32

        self.__peer: enet.Peer = None

    def connect(self, address: tuple[str, int] = None) -> None:
        self.__address = address or self.__address
        self.__peer = self.__host.connect(enet.Address(*self.__address), 2, 0)

    def start(self) -> None:
        self._event_loop.create_task(self.run())
        self._event_loop.run_forever()

    def send(self, packet: Packet = None, data: bytes = None) -> None:
        if data is not None:
            packet = Packet.from_bytes(data)

        self.__peer.send(0, packet.enet_packet)

    async def run(self) -> None:
        if self.__peer is None:
            self.connect()

        while True:
            event = self.__host.service(0, True)

            if event is None:
                await asyncio.sleep(0)
                continue

            ctx = Context()
            ctx.event = event
            ctx.client = self

            if event.type == enet.EVENT_TYPE_CONNECT:
                await self._dispatch(EventID.CONNECT, ctx)

            elif event.type == enet.EVENT_TYPE_RECEIVE:
                ctx.packet = Packet.from_bytes(event.packet.data)
                ctx.enet_packet = event.packet

                await self._dispatch(identify_packet(ctx.packet), ctx)
                await self._dispatch(EventID.RECEIVE, ctx)
            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                await self._dispatch(EventID.DISCONNECT, ctx)

            await asyncio.sleep(0)
