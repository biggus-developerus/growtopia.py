### FILE CONTAINS OLD CODE! ###	### FILE CONTAINS OLD CODE! ### ### FILE CONTAINS OLD CODE! ###
### FILE CONTAINS OLD CODE! ### ### FILE CONTAINS OLD CODE! ### ### FILE CONTAINS OLD CODE! ###
### FILE CONTAINS OLD CODE! ### ### FILE CONTAINS OLD CODE! ### ### FILE CONTAINS OLD CODE! ###

__all__ = ("GameClient",)


from context import (
    ClientContext,
)
from enet import (
    ENET_CRC32,
    EVENT_TYPE_CONNECT,
    EVENT_TYPE_DISCONNECT,
    EVENT_TYPE_RECEIVE,
    Host,
)
from inventory import (
    Inventory,
)
from utils import Buffer

from ..enums import EventID
from ..player import (
    PlayerLoginInfo,
)
from ..protocol import (
    HelloPacket,
    MessagePacket,
    PacketType,
    TextPacket,
    UpdatePacket,
)
from .client import Client


class GameClient(Client):
    def __init__(self, address: tuple[str, int], login_info: PlayerLoginInfo, **kwargs) -> None:
        super().__init__(address, **kwargs)

        self.login_info: PlayerLoginInfo = login_info
        self.inventory = Inventory()

    def send_to_server(self, port: int, token: int, user: int, string: str, lmode: bool) -> None:
        self.login_info.UUIDToken = (split_str := string.split("|"))[-1]
        self.login_info.token = token
        self.login_info.lmode = lmode
        self.login_info.user = user
        self.address = (split_str[0], port)

        self.disconnect(False)

        self.host = Host(
            self.host.peerCount,
            self.host.channelLimit,
            self.host.incomingBandwidth,
            self.host.outgoingBandwidth,
        )

        self.host.compress_with_range_coder()
        self.host.checksum = ENET_CRC32

        self.connect()

    # OLD CODE !!!
    async def _handle_event(self, context: ClientContext) -> bool:
        event = EventID.ON_UNKNOWN

        if context.enet_event.type == EVENT_TYPE_CONNECT:
            event = EventID.ON_CONNECT

        elif context.enet_event.type == EVENT_TYPE_DISCONNECT:
            event = EventID.ON_DISCONNECT
            self.running = False

        elif context.enet_event.type == EVENT_TYPE_RECEIVE:
            pck_type = Buffer(context.enet_event.packet.data).read_int()

            if pck_type == PacketType.HELLO:
                context.packet = HelloPacket.from_bytes(context.enet_event.packet.data)
                self.send(self.login_info.packet)

            elif pck_type == PacketType.TEXT:
                context.packet = TextPacket.from_bytes(context.enet_event.packet.data)
            elif pck_type == PacketType.GAME_MESSAGE:
                context.packet = MessagePacket.from_bytes(context.enet_event.packet.data)
            elif pck_type == PacketType.GAME_UPDATE:
                context.packet = UpdatePacket.from_bytes(context.enet_event.packet.data)

            event = context.packet.identify() if context.packet else EventID.ON_RECEIVE

            if event == EventID.OnSendToServer:
                variant_list = context.packet.get_variant_list()
                self.send_to_server(
                    variant_list[1].value,
                    variant_list[2].value,
                    variant_list[3].value,
                    variant_list[4].value,
                    variant_list[5].value,
                )

            elif event == EventID.ON_SEND_INVENTORY_STATE:
                self.inventory = Inventory.from_bytes(context.packet.extra_data)

        return await self.dispatch_event(event, context)
