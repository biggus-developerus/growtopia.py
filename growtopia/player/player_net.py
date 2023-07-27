__all__ = ("PlayerNet",)

from typing import Optional, Union

import enet

from ..dialog import Dialog
from ..items_data import ItemsData
from ..player_tribute import PlayerTribute
from ..protocol import (
    GameMessagePacket,
    GameUpdatePacket,
    GameUpdatePacketType,
    HelloPacket,
    StrPacket,
    VariantList,
)


class PlayerNet:
    """
    A base class for the Player class. This class is used to handle the networking bit of the Player class.

    Parameters
    ----------
    peer: enet.Peer
        The peer object of the player.

    Attributes
    ----------
    peer: enet.Peer
        The peer object of the player.
    last_packet_sent: Union[StrPacket, GameUpdatePacket]
        The last packet that was sent to the player.
    last_packet_received: Union[StrPacket, GameUpdatePacket]
        The last packet that was received from the player.
    """

    def __init__(self, peer: enet.Peer) -> None:
        self.peer: enet.Peer = peer

        self.last_packet_sent: Optional[Union[StrPacket, GameUpdatePacket]] = None
        self.last_packet_received: Optional[Union[StrPacket, GameUpdatePacket]] = None

    def _send(
        self, data: bytes = None, flags: int = enet.PACKET_FLAG_RELIABLE, enet_packet: enet.Packet = None
    ) -> bool:
        if not data and not enet_packet:
            raise ValueError("No data or packet was passed.")

        return (
            True
            if self.peer.send(0, enet_packet or enet.Packet(data, flags or enet.PACKET_FLAG_RELIABLE)) == 0
            else False
        )

    def send(self, packet: Union[StrPacket, GameUpdatePacket, HelloPacket]) -> bool:
        """
        Sends a packet to the player.

        Parameters
        ----------
        packet: Union[StrPacket, GameUpdatePacket, HelloPacket]
            The packet to send to the player.

        Returns
        -------
        bool:
            True if the packet was successfully sent, False otherwise.
        """
        if not isinstance(packet, (StrPacket, GameUpdatePacket, HelloPacket)):
            raise TypeError("Invalid packet type passed.")

        if self._send(enet_packet=packet.enet_packet):
            self.last_packet_sent = packet
            return True

        return False

    def send_log(self, message: str) -> bool:
        """
        Logs a message to the player.

        Parameters
        ----------
        message: str
            The message to log to the player.

        Returns
        -------
        bool:
            True if the packet was successfully sent, False otherwise.
        """
        return self.send(GameMessagePacket(f"action|log\nmsg|{message}").enet_packet)

    def reject_login(self, *args) -> bool:
        ...

    def on_console_message(self, message: str) -> bool:
        """
        Sends a console message to the player.

        Parameters
        ----------
        message: str
            The console message.

        Returns
        -------
        bool:
            True if the packet was successfully sent, False otherwise.
        """
        return self.send(
            GameUpdatePacket(
                update_type=GameUpdatePacketType.CALL_FUNCTION,
                variant_list=VariantList("OnConsoleMessage", message),
            )
        )

    # SOON!!!!

    def on_super_main(
        self,
        items_data_or_hash: Union[ItemsData, int],
        player_tribute_or_hash: Union[PlayerTribute, int],
        cdn_host: str,
        cdn_route: str,
        blocked_packages: str,
        settings: str,
        *,
        function_name: str = "OnSuperMainStartAcceptLogonHrdxs47254722215a",
    ) -> bool:
        """
        Sends the OSM packet to the player.

        Parameters
        ----------
        items_data_or_hash: Union[ItemsData, int]
            The items data or hash.
        player_tribute_or_hash: Union[PlayerTribute, int]
            The player tribute or hash.
        cdn_host: str
            The CDN host.
        cdn_route: str
            The CDN route.
        blocked_packages: str
            The blocked packages.
        settings: str
            The settings.

        Kwargs
        ------
        function_name: str
            The function name. Could be set to communicate with older clients, as the function's name is different.

        Returns
        -------
        bool:
            True if the packet was successfully sent, False otherwise.
        """
        if isinstance(items_data_or_hash, ItemsData):
            items_data_or_hash = items_data_or_hash.hash

        if isinstance(player_tribute_or_hash, PlayerTribute):
            player_tribute_or_hash = player_tribute_or_hash.hash

        return self.send(
            GameUpdatePacket(
                update_type=GameUpdatePacketType.CALL_FUNCTION,
                variant_list=VariantList(
                    function_name,
                    items_data_or_hash,
                    cdn_host,
                    cdn_route,
                    blocked_packages,
                    settings,
                    player_tribute_or_hash,
                ),
            )
        )

    def on_send_to_server(self, port: int, token: int, user: int, string: str, lmode: bool) -> bool:
        """
        Sends the client to a sub server.

        Parameters
        ----------
        port: int
            The port of the sub server
        token: int
            The token that the client will be using for authentication.
        user: int
        string: str
            The string is made up of 3 value pairs. (host|doorid|uuidtoken)
        lmode: bool
            Is the client being sent to this sub server whilst being in a world or not.

        Returns
        -------
        bool:
            True if the packet was successfully sent, False otherwise.
        """
        return self.send(
            GameUpdatePacket(
                update_type=GameUpdatePacketType.CALL_FUNCTION,
                variant_list=VariantList(
                    "OnSendToServer",
                    port,
                    token,
                    user,
                    string,
                    lmode,
                ),
            )
        )

    def on_dialog_request(self, dialog: Dialog) -> bool:
        raise NotImplementedError

    def on_request_world_select_menu(self, *args) -> bool:
        # TODO: new helper class, WorldSelectMenu 🤯🤯🤯🤯
        raise NotImplementedError

    def disconnect(self, text: Optional[str] = None) -> None:
        """
        Disconnects the player.

        Parameters
        ----------
        text: str
            The text to send to the player before disconnecting them.
        """
        if text:
            self.send_log(text)

        self.peer.disconnect()
