__all__ = ("Server",)

import enet
from .host import Host


class Server(Host):
    """
    Represents a Growtopia server. This class uses the Host class as a base class and extends its functionality.
    This class is used as a base class for other types of servers, such as ProxyServer and LoginServer.

    Parameters
    ----------
    address: tuple[str, int]
        The address to bind the server to.

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

    Attributes
    ----------
    players: dict[int, Player]
        A dictionary of all the players connected to the server.
    """

    def __init__(
        self,
        address: tuple[str, int],
        **kwargs,
    ) -> None:
        super().__init__(
            enet.Address(*address),
            kwargs.get("peer_count", 32),
            kwargs.get("channel_limit", 2),
            kwargs.get("incoming_bandwidth", 0),
            kwargs.get("outgoing_bandwidth", 0),
        )

        # self.players: dict[int, Player] = {}
