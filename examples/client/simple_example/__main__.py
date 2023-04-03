import growtopia

client = growtopia.Client(("127.0.0.1", 10000))


@client.listener
async def on_client_ready(ctx: growtopia.Context):
    print("The client is now running!")


@client.listener
async def on_connect(ctx: growtopia.Context):
    print(f"Successfully connected to the server at {ctx.peer.address}!")


@client.listener
async def on_hello(ctx: growtopia.Context):
    print("Got the hello packet from the server!")


@client.listener
async def on_disconnect(ctx: growtopia.Context):
    print(f"Disconnected from the server at {ctx.peer.address}!")


@client.listener
async def on_receive(ctx: growtopia.Context):
    print(f"Received a packet from the server: {ctx.enet_packet.data}")


client.start()
