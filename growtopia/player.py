__all__ = ("Player",)

import enet

from .player_net_funcs import _PlayerNetworkFunctions


class Player(_PlayerNetworkFunctions):
    def __init__(self, peer: enet.Peer) -> None:
        self.peer: enet.Peer = peer
        self.address: enet.Address = peer.address
