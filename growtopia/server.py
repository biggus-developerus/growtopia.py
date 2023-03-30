__all__ = ("Server",)

import asyncio
from typing import Optional

import enet

from .context import Context
from .enums import EventID
from .player import Player
from .pool import Pool
from .protocol import Packet
from .utils import identify_packet


class Server(Pool, enet.Host):
    def __init__(self, address: tuple[str, int], **kwargs) -> None:
        Pool.__init__(self)
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

        self.__players: dict[str, Player] = {}

    def get_player(self, address: str) -> Optional[Player]:
        return self.__players.get(address, None)

    def add_player(self, player: Player) -> None:
        self.__players[str(player.address)] = player

    def remove_player(self, player: Player) -> None:
        self.__players.pop(str(player.address), None)

    def start(self) -> None:
        self._event_loop.create_task(self.run())
        self._event_loop.run_forever()

    async def run(self) -> None:
        ctx = Context()
        ctx.server = self

        await self._dispatch(EventID.SERVER_READY, ctx)

        while True:
            event = self.service(0, True)

            if event is None:
                await asyncio.sleep(0)
                continue

            ctx = Context()

            ctx.event = event
            ctx.server = self

            if event.type == enet.EVENT_TYPE_CONNECT:
                player = Player(event.peer)
                self.add_player(player)

                ctx.peer = event.peer
                ctx.player = player

                await self._dispatch(EventID.CONNECT, ctx)

            elif event.type == enet.EVENT_TYPE_RECEIVE:
                ctx.peer = event.peer
                ctx.enet_packet = event.packet
                ctx.player = self.get_player(str(event.peer.address))

                ctx.packet = Packet.from_bytes(event.packet.data)

                await self._dispatch(identify_packet(ctx.packet), ctx)
                await self._dispatch(EventID.RECEIVE, ctx)
            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                ctx.player = self.get_player(str(event.peer.address))
                ctx.peer = event.peer
                await self._dispatch(EventID.DISCONNECT, ctx)
