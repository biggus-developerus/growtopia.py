__all__ = ("HTTP",)

from typing import Tuple
from urllib.parse import (
    urljoin,
)

from aiohttp import (
    ClientResponse,
    ClientSession,
)

from ..utils import Buffer
from .constants import (
    UBI_CDN,
    UBI_CDN_PATH,
    UBI_PC32_USER_AGENT,
)


class HTTP:
    @staticmethod
    async def get(base_url: str, path: str, **kwargs) -> Tuple[ClientResponse, Buffer]:
        async with ClientSession(base_url=base_url) as session:
            async with session.get(path, **kwargs) as r:
                return r, Buffer(bytearray(await r.read()))

    @staticmethod
    async def fetch_file_from_cdn(
        file_path: str,
        *,
        keep_path: bool = False,
        cdn_url: str = UBI_CDN,
        cdn_path: str = UBI_CDN_PATH,
    ) -> Buffer:
        if not keep_path and len(file_path.split("/")) == 1:
            file_path = "game/" + file_path

        route = urljoin(cdn_path, file_path)

        r, buffer = await HTTP.get(
            cdn_url,
            route,
            headers={"User-Agent": UBI_PC32_USER_AGENT},
        )

        if r.status != 200:
            return Buffer()

        return buffer
