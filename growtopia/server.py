__all__ = ("Server",)

import asyncio

import enet

from .context import Context
from .enums import EventID
from .pool import Pool


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
                ctx.peer = event.peer
                await self._dispatch(EventID.CONNECT, ctx)

            elif event.type == enet.EVENT_TYPE_RECEIVE:
                ctx.peer = event.peer
                ctx.enet_packet = event.packet
                await self._dispatch(EventID.RECEIVE, ctx)
            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                ctx.peer = event.peer
                await self._dispatch(EventID.DISCONNECT, ctx)

    def start(self) -> None:
        self._event_loop.create_task(self.run())
        self._event_loop.run_forever()
