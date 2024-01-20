__all__ = ("PlayerTribute",)

from ..utils import (
    File,
    ReadBuffer,
    WriteBuffer,
)


class PlayerTribute(File):
    def __init__(self, path: str) -> None:
        if not File.is_player_tribute(path):
            raise ValueError("File is not player_tribute.dat")

        self.buffer: ReadBuffer = ReadBuffer.load_file(path)

        self.version: int = 0
        self.hash: int = 0

    def parse(self) -> None:
        self.hash = self._get_hash()

    def serialise(self, overwrite_read_buff: bool = False) -> ReadBuffer:
        write_buffer = WriteBuffer()

        read_buffer = ReadBuffer.load_bytes(write_buffer.data)

        if overwrite_read_buff:
            self.buffer = read_buffer

        return read_buffer

    def save(self, path: str) -> None:
        self.serialise(True)  # overwrite read buffer (self.buffer)
        super().save(path)  # save file

    def __repr__(self) -> str:
        return f"<PlayerTribute version={self.version} hash={self.hash}>"

    def __str__(self) -> str:
        return repr(self)
