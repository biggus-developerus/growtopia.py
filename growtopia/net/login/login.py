__all__ = ("Login",)

from json.decoder import (
    JSONDecodeError,
    JSONDecoder,
)
from urllib.parse import quote

from aiohttp import (
    ClientSession,
)
from bs4 import (
    BeautifulSoup,  # For scraping the login redirect URLS & token
)

from .enums import (
    AccountType,
    WebActionType,
)
from .login_data import (
    LoginData,
)


# TODO: Holy fuck make this fucking better??? Why did I even write this fucking dog wank (You can't do any better, that's why, Jakob.) :'(
class Login:
    def __init__(
        self,
        account_type: AccountType,
        login_data: LoginData,
        *,
        scheme: str = "https://",
        fqdn: str = "login.growtopiagame.com",
        action_urls: dict[WebActionType, str] = {
            WebActionType.NEW_SESSION: WebActionType.NEW_SESSION.value,
            WebActionType.CLOSE_SESSION: WebActionType.CLOSE_SESSION.value,
            WebActionType.GROWID_VALIDATE: WebActionType.GROWID_VALIDATE.value,
        },
    ) -> None:
        self._account_type: AccountType = account_type
        self._login_data: LoginData = login_data

        self._scheme: str = scheme
        self._fqdn: str = fqdn
        self._action_urls: dict[WebActionType, str] = action_urls

        self._urls: dict[AccountType, str | None] = {}
        self._token: tuple[str, str] | None = None

        self._aiohttp_sess: ClientSession | None = None
        self._login_result: bool | dict = False

    def get_login_result(self) -> bool | dict:
        return self._login_result

    def _join(self, action_type: WebActionType) -> str:
        return self._scheme + self._fqdn + self._action_urls[action_type]

    async def _new_aiohttp_sess(self) -> None:
        if self._aiohttp_sess and not self._aiohttp_sess.closed:
            await self._aiohttp_sess.close()

        self._aiohttp_sess = ClientSession()

    async def _close_aiohttp_sess(self) -> None:
        if not self._aiohttp_sess or self._aiohttp_sess.closed:
            return

        await self._aiohttp_sess.close()
        self._aiohttp_sess = None

    async def _new_session(self) -> bool:
        await self._new_aiohttp_sess()

        url = self._join(WebActionType.NEW_SESSION)
        login_data = self._login_data.url_encode()

        data: bytes | None = None
        async with self._aiohttp_sess.post(url=url, data=login_data) as r:
            if r.status != 200:
                r.raise_for_status()

            # yeah idk y but the content-type is never set to application/json so we gotta do this shit instead :O!
            data = await r.content.read()

            try:
                json_data = JSONDecoder().decode(data.decode())
                if json_data.get("status") == "failed":
                    data = None
            except JSONDecodeError:
                pass

        if not data:
            return False

        s = BeautifulSoup(data, features="html.parser")
        if not (apngo_urls := s.find_all("a", class_="btn btn-block")) or len(apngo_urls) < 2:
            return False

        if not (growid := s.find("a", class_="grow-login btn btn-block")):
            return False

        apple, google, *_ = apngo_urls

        self._urls = {
            AccountType.APPLE: apple.get("href", None),
            AccountType.GOOGLE: google.get("href", None),
            AccountType.GROWID: growid.get("href", None),
        }

        return True

    async def _get_token(self) -> bool:
        if not self._aiohttp_sess:
            raise ValueError(
                "Start a new session first before attempting to retrieve the login token."
            )

        if not (url := self._urls.get(self._account_type, None)):
            return False

        data: bytes | None = None
        async with self._aiohttp_sess.get(url=url) as r:
            if r.status != 200:
                r.raise_for_status()

            data = await r.content.read()

        if not data:
            return False

        parsed_html = BeautifulSoup(data, features="html.parser")
        inp = parsed_html.find("input")

        if not inp or not (name := inp.get("name", None)) or not (val := inp.get("value", None)):
            return False

        self._token = (name, val)
        return True

    async def _validate_growid(self, growid: str, password: str) -> bool:
        if not self._aiohttp_sess:
            raise ValueError("Start a new session first before attempting to validate growid.")
        elif not self._token:
            raise ValueError("Retrieve the token before attempting to validate growid.")

        url = self._join(WebActionType.GROWID_VALIDATE)

        data: bytes | None = None
        json_data: dict | None = None
        async with self._aiohttp_sess.post(
            url=url,
            data=f"{self._token[0]}={quote(self._token[1])}&growId={quote(growid)}&password={quote(password)}".encode(),
            headers={
                "Referer": self._urls[self._account_type],  # it sometimes needs this 😒
                "Content-Type": "application/x-www-form-urlencoded",
            },
        ) as r:
            if r.status != 200:
                r.raise_for_status()

            data = await r.content.read()
            try:
                json_data = JSONDecoder().decode(data.decode())
            except JSONDecodeError:
                data = None

        if not json_data or json_data.get("message") == "failed":
            return False

        self._login_result = json_data

        return True

    async def growid_login(self, growid: str, password: str) -> dict | bool:
        if not await self._new_session():
            return False

        if not await self._get_token():
            return False

        await self._validate_growid(growid, password)
        await self._close_aiohttp_sess()

        return self.get_login_result()
