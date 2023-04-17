__all__ = ("Server",)

import asyncio
from typing import Optional

import enet

from .context import Context
from .enums import EventID
from .event_pool import EventPool
from .items_data import ItemsData
from .player_pool import PlayerPool
from .player_tribute import PlayerTribute
from .protocol import Packet
from .utils import identify_packet


class Server(EventPool, PlayerPool, enet.Host):
    def __init__(
        self,
        address: tuple[str, int],
        items_data: Optional[ItemsData] = None,
        player_tribute: Optional[PlayerTribute] = None,
        **kwargs,
    ) -> None:
        EventPool.__init__(self)
        PlayerPool.__init__(self)
        enet.Host.__init__(
            self,
            enet.Address(*address),
            kwargs.get("max_peers", 32),
            kwargs.get("channels", 2),
            kwargs.get("in_bandwidth", 0),
            kwargs.get("out_bandwidth", 0),
        )

        self.compress_with_range_coder()
        self.checksum = enet.ENET_CRC32

        self.items_data: Optional[ItemsData] = items_data or None
        self.player_tribute: Optional[PlayerTribute] = player_tribute or None

        self.__running: bool = True

    def start(self) -> None:
        self.__running = True
        self._event_loop.run_until_complete(self.run())

    def stop(self) -> None:
        self.__running = False

    async def run(self) -> None:
        (ctx := Context()).server = self
        await self._dispatch(EventID.SERVER_READY, ctx)

        while self.__running:
            event = self.service(0, True)

            if event is None:
                await asyncio.sleep(0)  # pass control back to the event loop
                continue

            ctx = Context()

            ctx.event = event
            ctx.server = self

            if event.type == enet.EVENT_TYPE_CONNECT:
                ctx.player = self.new_player(event.peer)
                ctx.peer = event.peer

                await self._dispatch(EventID.CONNECT, ctx)

            elif event.type == enet.EVENT_TYPE_RECEIVE:
                ctx.peer = event.peer
                ctx.enet_packet = event.packet
                ctx.player = self.get_player(str(event.peer.address))

                ctx.packet = Packet.from_bytes(event.packet.data)

                await self._dispatch(identify_packet(ctx.packet), ctx)
                await self._dispatch(EventID.RECEIVE, ctx)
            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                ctx.player = self.remove_player(str(event.peer.address))
                ctx.peer = event.peer
                await self._dispatch(EventID.DISCONNECT, ctx)

        await self._dispatch(EventID.SERVER_CLEANUP, ctx)
