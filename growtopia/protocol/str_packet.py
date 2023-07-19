__all__ = ("StrPacket",)

from typing import Optional

from ..enums import EventID
from ..error_manager import ErrorManager
from ..exceptions import PacketTooSmall, PacketTypeDoesNotMatchContent
from .enums import PacketType
from .packet import Packet


class StrPacket(Packet):
    """
    This class is used as base by classes that represent packets that contain text (i.e TextPacket and GameMessagePacket)

    Parameters
    ----------
    text: Optional[str]
        The text to instantiate the string packet with.

    Kwargs
    ------
    type_: Optional[PacketType]
        The type of the string packet. This kwarg is already passed by the child classes TextPacket & GameMessagePacket.

    Attributes
    ----------
    _type: PacketType
        The type of the string packet.
    text: str
        The text that the packet holds.
    action: str
        The action from the text.
    arguments: dict[str, str]
        Action arguments from the text.
    kvps: dict[str, str]
        Key value pairs from the text. (key1|value2\nkey2|value2 -> {"key1": "value1", "key2": "value2"})
    data: bytearray
        The data that the packet holds.
    enet_packet: enet.Packet
        An enet.Packet object instantiated with the data that the packet's holding (flag: PACKET_FLAG_RELIABLE).
    """

    def __init__(self, text: Optional[str] = None, *, type_: Optional[PacketType] = None) -> None:
        super().__init__()

        self._type = type_ or PacketType.CONTAINS_TEXT

        self.text: str = text or ""

        self.action: str = ""
        self.arguments: dict[str, str] = {}  # arguments for the action
        self.kvps: dict[str, str] = {}  # general key-value pairs (login packet)

    def serialise(self) -> bytes:
        """
        Serialises the packet.

        Returns
        -------
        bytearray:
            The data the packet's holding (after serialisation)
        """
        self.data = bytearray(self._type.to_bytes(4, "little"))

        if self.action:
            self.text = f"action|{self.action}\n" + "\n".join(
                [f"{key}|{value}" for key, value in self.arguments.items()]
            )
        elif self.kvps:
            self.text = "\n".join([f"{key}|{value}" for key, value in self.kvps.items()])

        self.data += (self.text + ("\n" if not self.text.endswith("\n") else "")).encode()

        return bytes(self.data)

    def identify(self) -> EventID:
        """
        Identifies the packet's listener based on the packet's contents.

        Returns
        -------
        EventID
            The event ID responsible for handling the packet.
        """
        if self._malformed:
            return EventID.ON_MALFORMED_PACKET
        if "requestedName" in self.text:
            return EventID.ON_LOGIN_REQUEST
        if self.action:
            return EventID(f"on_{self.action}")

    @classmethod
    def from_bytes(cls, data: bytes) -> Optional["StrPacket"]:
        """
        Deserialises a packet from the bytes given. Returns a StrPacket object.

        Parameters
        ----------
        data: bytes
            The data to deserialise and make a StrPacket object out of.

        Raises
        ------
        TypeError:
            If the data wasn't of type bytes.
        PacketTooSmall:
            If the data was too small (<4)
        PacketTypeDoesNotMatchContent:
            If the data did not match the packet's type (TEXT/GAME_MESSAGE)

        Returns
        -------
        Optional["StrPacket"]
            Returns a StrPacket object when the deserialisation is successful, returns None otherwise.
        """
        str_packet = cls()

        if not isinstance(data, bytes):
            ErrorManager._raise_exception(
                TypeError(f"classmethod from_bytes takes bytes, type {type(data)} was passed in.")
            )

            return

        if len(data) < 4:
            str_packet._malformed = True
            ErrorManager._raise_exception(PacketTooSmall(str_packet, len(data), ">=4"))
            return

        str_packet._type = PacketType(int.from_bytes(data[:4], "little"))

        if str_packet._type != PacketType.TEXT and str_packet._type != PacketType.GAME_MESSAGE:
            str_packet._malformed = True
            ErrorManager._raise_exception(PacketTypeDoesNotMatchContent(str_packet, str_packet._type))
            return

        str_packet.text = data[4:-1].decode()
        str_packet.data = data

        if str_packet.text.startswith("action"):
            for i in str_packet.text.split("\n"):
                if len((kvp := i.split("|"))) != 2:
                    continue

                key, value = kvp

                if key == "action":
                    str_packet.action = value
                    continue

                str_packet.arguments[key] = value

        elif "requestedName" in str_packet.text:
            str_packet.kvps = {kvp[0]: kvp[-1] for i in str_packet.text.split("\n") if (len(kvp := i.split("|")) == 2)}

        return str_packet
