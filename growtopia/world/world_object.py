__all__ = ("WorldObject",)


class WorldObject:
    def __init__(self) -> None:
        self.id: int = 0  # uint16
        self.pos: tuple[float, float] = (0.0, 0.0)
        self.count: int = 0  # uint8
        self.flags: int = 0  # uint8
        self.object_id: int = 0  # uint32

        self.data: bytearray = bytearray()

    def serialise(self) -> bytes:
        ...


"""

std::vector<uint8_t> World::PackObjects(const bool& to_database, bool Packet, float GameVersion) {
    std::vector<uint8_t> ret{};
    ret.resize(this->GetObjectsMemoryUsage(Packet, GameVersion));

    BinaryWriter buffer{ ret.data() };
    if (Packet && GameVersion >= 4.31f) {
        buffer.write<uint64_t>(0);
        buffer.write<uint32_t>(0);
    }
    buffer.write<uint32_t>(static_cast<uint32_t>(m_objects.size()));
    buffer.write<uint32_t>(m_object_id - (to_database ? 0 : 1));
    for (auto& [id, object] : m_objects) {
        buffer.write<uint16_t>(object.m_item_id);
        buffer.write<CL_Vec2f>(object.m_pos);
        buffer.write<uint8_t>(object.m_item_amount);
        buffer.write<uint8_t>(object.m_flags);
        buffer.write<uint32_t>(id);
    }
    return ret;
}

"""
