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

    packet.set_variant_list(
        protocol.VariantList("OnConsoleMessage", "Hello, world!", 5, 10.5, 69)
    )

    vlist_from_bytes = protocol.VariantList.from_bytes(packet.extra_data)

    assert len(vlist_from_bytes) == 5
    assert vlist_from_bytes[0].value == "OnConsoleMessage"
    assert vlist_from_bytes[1].value == "Hello, world!"
    assert vlist_from_bytes[2].value == 5
    assert vlist_from_bytes[3].value == 10.5
    assert vlist_from_bytes[4].value == 69


def test_login_packet_parse() -> None:
    """Parse a login packet."""

    d8a = b"\x02\x00\x00\x00tankIDName|.\ntankIDPass|.\nrequestedName|DawnDar\nf|1\nprotocol|188\ngame_version|4.2\nfz|0\nlmode|0\ncbits|1024\nplayer_age|69\nGDPR|1\ncategory|_-5100\ntotalPlaytime|0\nklv|0\nhash2|-0\nmeta|localhost\nfhash|-0\nrid|0\nplatformID|0,1,1\ndeviceVersion|0\ncountry|us\nhash|-0\nmac|0\nwk|0\nzf|0\x00"
    packet = protocol.Packet.from_bytes(d8a)

    assert packet.parse_login_packet() == {
        "tankIDName": ".",
        "tankIDPass": ".",
        "requestedName": "DawnDar",
        "f": "1",
        "protocol": "188",
        "game_version": "4.2",
        "fz": "0",
        "lmode": "0",
        "cbits": "1024",
        "player_age": "69",
        "GDPR": "1",
        "category": "_-5100",
        "totalPlaytime": "0",
        "klv": "0",
        "hash2": "-0",
        "meta": "localhost",
        "fhash": "-0",
        "rid": "0",
        "platformID": "0,1,1",
        "deviceVersion": "0",
        "country": "us",
        "hash": "-0",
        "mac": "0",
        "wk": "0",
        "zf": "0",
    }


if __name__ == "__main__":
    test_hello_packet()
    test_text_packet()
    test_game_message_packet()
    test_game_packet()
