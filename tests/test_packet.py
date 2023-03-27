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

    packet.set_variant_list(protocol.VariantList("OnConsoleMessage", "Hello, world!"))

    vlist_from_bytes = protocol.VariantList.from_bytes(packet.extra_data)

    assert len(vlist_from_bytes) == 2
    assert vlist_from_bytes[0].value == "OnConsoleMessage"
    assert vlist_from_bytes[1].value == "Hello, world!"


if __name__ == "__main__":
    test_hello_packet()
    test_text_packet()
    test_game_message_packet()
    test_game_packet()
