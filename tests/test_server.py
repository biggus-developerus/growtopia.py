"""Test the Server class."""

from growtopia import ServerContext, GameServer


def test_server() -> None:
    """Test the server"""

    server = GameServer(
        address=("127.0.0.1", 17095),
    )

    @server.listener
    async def on_connect(context: ServerContext) -> None:
        ...

    # server.start() TODO: Allow the server to run for a couple of seconds and then stop it.


if __name__ == "__main__":
    test_server()
