__all__ = ("Host",)

import enet

# TODO:
# - Implement some concrete methods for the Host class. (e.g override broadcast to send protocol.Packet objects, strings or bytes instead of enet.Packet objects)


class Host(enet.Host):
    """
    Represents an enet.Host object. This class uses the enet.Host class as a base class and extends its functionality.

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

    def start(self) -> None:
        """
        Runs the coroutine that starts the asynchronous loop.

        Returns
        -------
        None

        NotImplementedError
            If this method is not overridden. (e.g not implemented in a subclass)
        """

        raise NotImplementedError

    def stop(self) -> None:
        """
        Stops the running asynchronous loop and dispatches the on_cleanup event.

        Returns
        -------
        None

        NotImplementedError
            If this method is not overridden. (e.g not implemented in a subclass)
        """

        raise NotImplementedError

    async def run(self) -> None:
        """
        Starts an asynchronous loop that handles events accordingly.

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            If this method is not overridden. (e.g not implemented in a subclass)
        """

        raise NotImplementedError
