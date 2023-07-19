__all__ = ("GameClient",)

import asyncio

import enet

from ..context import ClientContext
from ..enums import EventID
from ..inventory import Inventory
from ..items_data import ItemsData
from ..player import PlayerLoginInfo
from ..protocol import (
    GameMessagePacket,
    GameUpdatePacket,
    HelloPacket,
    Packet,
    PacketType,
    TextPacket,
)
from .client import Client


class GameClient(Client):
    """
    Represents a Growtopia game client. Uses the Client class as base.

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

    def __init__(self, address: tuple[str, int], login_info: PlayerLoginInfo, **kwargs) -> None:
        super().__init__(address, **kwargs)

        self.login_info: PlayerLoginInfo = login_info
        self.inventory: Inventory = Inventory()

        # these attributes will be used when creating a new host (OnSendToServer)
        self.__peer_count = kwargs.get("peer_count", 1)
        self.__channel_limit = kwargs.get("channel_limit", 2)
        self.__incoming_bandwidth = kwargs.get("incoming_bandwidth", 0)
        self.__outgoing_bandwidth = kwargs.get("outgoing_bandwidth", 0)

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

            if event.type == enet.EVENT_TYPE_CONNECT:
                await self.dispatch_event(EventID.ON_CONNECT, context)
                continue

            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                await self.dispatch_event(EventID.ON_DISCONNECT, context)
                self.running = False

            elif event.type == enet.EVENT_TYPE_RECEIVE:
                if (type_ := Packet.get_type(event.packet.data)) == PacketType.HELLO:
                    context.packet = HelloPacket.from_bytes(event.packet.data)
                    self.send(self.login_info.packet)

                elif type_ == PacketType.TEXT:
                    context.packet = TextPacket.from_bytes(event.packet.data)
                elif type_ == PacketType.GAME_MESSAGE:
                    context.packet = GameMessagePacket.from_bytes(event.packet.data)
                elif type_ == PacketType.GAME_UPDATE:
                    context.packet = GameUpdatePacket.from_bytes(event.packet.data)

                event = context.packet.identify() if context.packet else EventID.ON_RECEIVE

                if event == EventID.OnSendToServer:
                    variant_list = context.packet.get_variant_list()
                    port, token, user, string, lmode = (
                        variant_list[1].value,
                        variant_list[2].value,
                        variant_list[3].value,
                        variant_list[4].value,
                        variant_list[5].value,
                    )

                    self.login_info.UUIDToken = (split_str := string.split("|"))[-1]
                    self.login_info.token = token
                    self.login_info.lmode = lmode
                    self.login_info.user = user

                    self._address = (split_str[0], port)
                    self.disconnect(False)

                    self._host = enet.Host(
                        None,
                        self.__peer_count,
                        self.__channel_limit,
                        self.__incoming_bandwidth,
                        self.__outgoing_bandwidth,
                    )

                    self._host.compress_with_range_coder()
                    self._host.checksum = enet.ENET_CRC32

                    self.connect()

                elif event == EventID.ON_SEND_INVENTORY_STATE:
                    self.inventory = Inventory.from_bytes(context.packet.extra_data)
                elif event == EventID.ON_SEND_ITEMS_DATA:
                    self.items_data = ItemsData.from_bytes(context.packet.extra_data)

                if not await self.dispatch_event(
                    event,
                    context,
                ):
                    await self.dispatch_event(EventID.ON_UNHANDLED, context)

        await self.dispatch_event(
            EventID.ON_CLEANUP,
            context,
        )
