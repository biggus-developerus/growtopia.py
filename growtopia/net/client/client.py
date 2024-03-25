__all__ = ("Client",)


from abc import (
    ABC,
    abstractmethod,
)
from asyncio import run, sleep

from context import (
    ClientContext,
)

from ..dispatcher import (
    Dispatcher,
)
from ..enums import EventID
from .net_client import (
    NetClient,
)


class Client(NetClient, Dispatcher, ABC):
    def __init__(self, address: tuple[str, int], **kwargs) -> None:
        NetClient.__init__(self, address, **kwargs)
        Dispatcher.__init__(self)

        self.running: bool = False

    def start(self) -> None:
        run(self.run())

    def stop(self) -> None:
        self.running = False

    async def run(self) -> None:
        if self.peer is None:
            self.conenct()

        self.running = True

        await self.dispatch_event(EventID.ON_READY, self)

        while self.running:
            event = self.host.service(0, True)

            if event is None:
                sleep(0)
                continue

            context = ClientContext()
            context.client = self
            context.enet_event = event

            response = await self._handle_event(context)

            if not response:
                await self.dispatch_event(
                    EventID.ON_UNHANDLED, context
                )  # dispatch the ON_UNHANDLED event if the packet isn't handled by the user but recognised by growtopia.py

        await self.dispatch_event(EventID.ON_CLEANUP, self)

    @abstractmethod
    async def _handle_event(self, context: ClientContext) -> None: ...
