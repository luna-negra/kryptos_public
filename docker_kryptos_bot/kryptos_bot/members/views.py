from execute import bot
# do not edit above this line.
# please write down your code below.

from members.serializers import *


async def activation(types):
    sr = ActivateAccount(types=types, route="activation")
    await main_member(types=types) if await sr.check_activation() else await sr.send_message()
    return None


async def activate_account(types):
    sr = InputActivation(types=types, link_route="activation")

    if getattr(types, "data", None) == "send_code":
        await sr.send_code()

    if await sr.get_client_data():
        await main(types=types)

    return None


async def check_signin(types) -> bool:
    route = CLIENT_INFO[types.from_user.id].route
    data = getattr(types, "data", None)
    text = getattr(types, "text", None)
    if route == "" and (data is not None or text is not None):
        await bot.send_message(chat_id=types.from_user.id,
                               text=translate(domain="warnings",
                                              key="server_restarted",
                                              types=types))
        return False

    chat_id: int = types.from_user.id
    is_signin: bool = CLIENT_INFO[chat_id].is_signin
    is_active: bool = CLIENT_INFO[chat_id].info.get("is_active")

    if not is_signin:
        await bot.send_message(chat_id=chat_id,
                               text=translate(domain="warnings", key="require_signin", types=types))

    elif not is_active:
        await bot.send_message(chat_id=chat_id,
                               text=translate(domain="warnings", key="require_activation", types=types))

    return is_signin and is_active


async def main(types):
    sr = Main(types=types, route="main")
    await activation(types=types) if await sr.send_message() else await main_anon(types=types)
    return None


async def main_anon(types):
    sr = MainAnon(types=types, route="main_anon")
    await sr.send_message()
    return None


async def main_member(types):
    sr = MainMember(types=types, route="main_member")
    await sr.send_message()
    return None


async def signin(types):
    sr = SignIn(types=types, route="signin", link_route="main_anon")
    if await sr.get_client_data():
        await main(types=types)

    return None


async def signup(types):
    sr = SignUp(types=types, route="signup", link_route="main_anon")
    if await sr.get_client_data():
        await main(types=types)
    return None


async def signout(types):
    sr = SignOut(types=types, route="signout")
    await sr.send_message()
    await main(types=types)
    return None
