from growtopia import Collection, Context, Listener


class EnetEvents(Collection):
    def __init__(self) -> None:
        super().__init__()

    @Listener
    async def on_connect(self, ctx: Context):
        ctx.player.send(data=bytearray([1, 0, 0, 0]))
        print(f"{ctx.peer.address} has connected to the server!")

    @Listener
    async def on_receive(self, ctx: Context):
        print(f"{ctx.peer.address} sent a packet with type {ctx.packet.type}")

    @Listener
    async def on_disconnect(self, ctx: Context):
        print(f"{ctx.peer.address} has disconnected from the server!")
