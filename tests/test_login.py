from asyncio import run

import pytest

from growtopia import (
    AccountType,
    Login,
    LoginData,
)


@pytest.mark.asyncio
async def test_login():
    login_info = LoginData(game_version="4.62")  
    # The only required field is game_version;
    # the rest can remain empty.
    # I'm unsure if this also applies
    # when authenticating to a game server. 🤷‍♂️🤷‍♂️

    login = Login(AccountType.GROWID, login_info)
    assert not await login.growid_login("invalid_usr", "invalid_psw")

    # assert await login.growid_login("valid_usr", "valid_psw")
    # assert login.get_login_result().get("status", None) == "success"
    # assert login.get_login_result().get("message", None) == "Account Validated."
    # assert login.get_login_result().get("accountType", None) == "growtopia"
    # assert login.get_login_result().get("token", None) != None


if __name__ == "__main__":
    run(test_login())
