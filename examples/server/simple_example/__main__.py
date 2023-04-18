import growtopia

server = growtopia.Server(("127.0.0.1", 10000))


@server.listener
async def on_server_ready(ctx: growtopia.Context):
    print(f"The server is now running on {ctx.server.address}")


@server.listener
async def on_connect(ctx: growtopia.Context):
    print(f"{ctx.peer.address} has connected to the server!")


@server.listener
async def on_disconnect(ctx: growtopia.Context):
    print(f"{ctx.peer.address} has disconnected from the server!")


@server.listener
async def on_receive(ctx: growtopia.Context):
    print(f"{ctx.peer.address} sent a packet: {ctx.enet_packet.data}")


server.start()
