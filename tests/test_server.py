"""Test the Server class."""

from growtopia import ServerContext, GameServer, ItemsData, PlayerTribute


def test_server() -> None:
    """Test the server"""

    items_data = ItemsData("data/items_v15.dat")
    player_triute = PlayerTribute("data/player_tribute_v2.dat")

    server = GameServer(
        ("127.0.0.1", 17095),
        items_data,
        player_triute,
    )

    @server.listener
    async def on_connect(context: ServerContext) -> None:
        ...

    # server.start() TODO: Allow the server to run for a couple of seconds and then stop it.


if __name__ == "__main__":
    test_server()
