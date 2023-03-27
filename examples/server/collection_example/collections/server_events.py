from growtopia import Collection, Context, Listener
from growtopia import protocol


class ServerEvents(Collection):
    def __init__(self) -> None:
        super().__init__()

    @Listener
    async def on_server_ready(self, ctx: Context):
        print(f"The server is now running on {ctx.server.address}")

    @Listener
    async def on_login_request(self, ctx: Context):
        packet = protocol.Packet()

        packet.type = protocol.PacketType.GAME_PACKET
        packet.game_packet_type = protocol.GamePacketType.CALL_FUNCTION

        packet.set_variant_list(protocol.VariantList("OnConsoleMessage", "No..."))

        ctx.player.send(packet=packet)

    @Listener
    async def on_quit(self, ctx: Context):
        print(f"{ctx.peer.address} has quit the server!")
