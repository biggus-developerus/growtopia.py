"""Test the Server class."""

from growtopia import Context, Server


def test_server() -> None:
    """Test the server"""

    server = Server(
        address=("127.0.0.1", 17095),
    )

    @server.listener
    async def on_connect(context: Context) -> None:
        print("on_connect")
        print(context)

    # server.start() TODO: Allow the server to run for a couple of seconds and then stop it.


if __name__ == "__main__":
    test_server()
