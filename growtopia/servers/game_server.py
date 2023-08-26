__all__ = ("GameServer",)

import enet

from ..context import ServerContext
from ..enums import EventID
from ..player import PlayerLoginInfo
from ..protocol import (
    GameMessagePacket,
    GameUpdatePacket,
    HelloPacket,
    Packet,
    PacketType,
    TextPacket,
)
from .server import Server
from .server_world_pool import ServerWorldPool
from ..obj_holder import _ObjHolder


class GameServer(Server, ServerWorldPool):
    def __init__(self, address: tuple[str, int], **kwargs) -> None:
        Server.__init__(self, address, **kwargs)
        ServerWorldPool.__init__(self)

        self._send_hello: bool = kwargs.get("send_hello", True)

    async def _handle_event(self, context: ServerContext) -> bool:
        event = EventID.ON_UNKNOWN

        context.items_data = _ObjHolder.items_data
        context.player_tribute = _ObjHolder.player_tribute

        if context.enet_event.type == enet.EVENT_TYPE_CONNECT:
            context.player = self.new_player(context.enet_event.peer)

            if self._send_hello:
                context.player.send(HelloPacket())

            event = EventID.ON_CONNECT

        elif context.enet_event.type == enet.EVENT_TYPE_DISCONNECT:
            context.player = self.get_player(context.enet_event.peer)
            self.remove_player(context.enet_event.peer)

            event = EventID.ON_DISCONNECT

        elif context.enet_event.type == enet.EVENT_TYPE_RECEIVE:
            context.player = self.get_player(context.enet_event.peer)
            packet_type = Packet.get_type(context.enet_event.packet.data)

            if context.player.world:
                context.world = context.player.world

            if packet_type == PacketType.TEXT:
                context.packet = TextPacket.from_bytes(context.enet_event.packet.data)
            elif packet_type == PacketType.GAME_MESSAGE:
                context.packet = GameMessagePacket.from_bytes(context.enet_event.packet.data)
            elif packet_type == PacketType.GAME_UPDATE:
                context.packet = GameUpdatePacket.from_bytes(context.enet_event.packet.data)

            if context.packet is None:
                return False  # Do something here to alert the user.. no idea what to do yet.

            context.packet.sender = context.player
            event = context.packet.identify() if context.packet else EventID.ON_RECEIVE

            context.player.last_packet_received = context.packet

            if event == EventID.ON_LOGIN_REQUEST:
                context.player.login_info = PlayerLoginInfo(**context.packet.kvps)

                # I'd make it so that we send the OSM internally too, just like the hello packet.. but that might tamper with the API user's setup.
                # E.g the API user might have to send an asynchronous request to fetch the player's data and blah blah blah, if we send the OSM
                # before that's done, the client might send the enter_game packet and mess stuff up.

                # That would make the player look like they're trying to get into the game without waiting for validation from the server.
                # The validation being the OSM packet. For us to send it beforehand it'd mean that the server has accepted their data and
                # allowed them to enter the game.

                # This would happen only if the user was actually abiding by the asynchronous rules (in this case, they sent the request asynchronously.)

            elif event == EventID.ON_DIALOG_RETURN:
                if dialog_name := context.packet.arguments.get("dialog_name", None):
                    return await self.dispatch_dialog_return(
                        dialog_name,
                        context.packet.arguments.get("buttonClicked", None),
                        context,
                    )

            elif event == EventID.ON_INPUT:
                if (text := context.packet.arguments.get("text", None)) and text.startswith("/"):
                    if await self.dispatch_command((splt_txt := text.split(" "))[0][1:], splt_txt[1:], context):
                        return True  # so that we don't dispatch the ON_INPUT event.

            elif event == EventID.ON_TILE_CHANGE_REQUEST:
                context.tile = context.world.get_tile(context.packet.int_x, context.packet.int_y)
                context.item = _ObjHolder.items_data.get_item(context.packet.int)

        return await self.dispatch_event(event, context)
