__all__ = ("Host",)

import asyncio
import time

import enet


class Host(enet.Host):
    """
    Represents an enet.Host object. This classes uses the enet.Host class as a base class and extends its functionality.

    Parameters
    ----------
    address: enet.Address
        The address to bind the host to.
    peer_count: int
        The maximum amount of peers that can connect to the host.
    channel_limit: int
        The maximum amount of channels that can be used.
    incoming_bandwidth: int
        The maximum incoming bandwidth.
    outgoing_bandwidth: int
        The maximum outgoing bandwidth.

    Attributes
    ----------
    address: enet.Address
        The address that the host is bound to.
    peer_count: int
        The maximum amount of peers that can connect to the host.
    channel_limit: int
        The maximum amount of channels that can be used.
    incoming_bandwidth: int
        The maximum incoming bandwidth.
    outgoing_bandwidth: int
        The maximum outgoing bandwidth.
    peers: dict[int, enet.Peer]
        A dictionary that keeps track of all connected peers. Connection IDs are used as keys and enet.Peer objects are used as values.
    """

    def __init__(
        self,
        address: enet.Address,
        peer_count: int,
        channel_limit: int,
        incoming_bandwidth: int,
        outgoing_bandwidth: int,
    ) -> None:
        super().__init__(
            address,
            peer_count,
            channel_limit,
            incoming_bandwidth,
            outgoing_bandwidth,
        )

        self.address: enet.Address = address
        self.peer_count: int = peer_count
        self.channel_limit: int = channel_limit
        self.incoming_bandwidth: int = incoming_bandwidth
        self.outgoing_bandwidth: int = outgoing_bandwidth

        self.peers: dict[int, enet.Peer] = {}
        self.lost_events: list[enet.Event] = []
        self.__running: bool = False

    def start(self) -> None:
        """
        Run the asyncio event loop.

        Returns
        -------
        None
        """
        asyncio.run(self.run())

    async def run(self) -> None:
        """
        Starts an asynchroneous loop that handles events accordingly.

        Returns
        -------
        None
        """
        self.__running = True
        while self.__running:
            res = (
                self._handle(event)
                if (event := self.service(0, True))
                else await asyncio.sleep(
                    0
                )  # pass control back to the event loop to prevent blocking and allow other tasks to run
            )

            if not res and res is not None:
                self.lost_events.append(event)

    async def _handle(self, event: enet.Event) -> None:
        """
        Handles event data accordingly.

        Parameters
        ----------
        event: enet.Event
            The event to dispatch.

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            If this method is not overridden. (e.g not implemented in a subclass)
        """
        raise NotImplementedError
