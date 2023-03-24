"""Test the packet class (assemble and disassemble)."""


from growtopia import protocol


def test_hello_packet() -> None:
    """Assemble and disassemble a hello packet."""

    packet = protocol.Packet()
    packet.type = protocol.PacketType.HELLO

    assert (
        protocol.Packet.from_bytes(packet.serialise()).type == protocol.PacketType.HELLO
    )


def test_text_packet() -> None:
    """Assemble and disassemble a text packet."""

    packet = protocol.Packet()

    packet.type = protocol.PacketType.TEXT
    packet.text = "Hello, world!"

    assert protocol.Packet.from_bytes(packet.serialise()).text == "Hello, world!"


def test_game_message_packet() -> None:
    """Assemble and disassemble a game message packet."""

    packet = protocol.Packet()

    packet.type = protocol.PacketType.GAME_MESSAGE
    packet.game_message = "Hello, world!"

    assert (
        protocol.Packet.from_bytes(packet.serialise()).game_message == "Hello, world!"
    )


def test_game_packet() -> None:
    "Assemble and disassemble a game packet."

    packet = protocol.Packet()

    packet.type = protocol.PacketType.GAME_PACKET
    packet.game_packet_type = protocol.GamePacketType.CALL_FUNCTION
    packet.flags = protocol.GamePacketFlags.EXTRA_DATA

    packet.extra_data = (
        vlist_data := protocol.VariantList("OnConsoleMessage", "Hello, world!").data
    )
    packet.extra_data_size = len(vlist_data)

    # Wait until I add a way to convert bytes to a variant list. (from_bytes function)


if __name__ == "__main__":
    test_hello_packet()
    test_text_packet()
    test_game_message_packet()
    test_game_packet()
