from execute import bot
# do not edit above this line.
# please write down your code below.

from members.views import main, check_signin
from settings.serializers import *


async def change_language(types):
    sr = ChangeLanguage(types=types, route="change_language")
    if await sr.send_message():
        await show_settings(types=types)
    return None


async def change_name(types):
    sr = ChangeName(types=types, route="change_name")
    await sr.send_message()
    return None


async def change_first_name(types):
    sr = ChangeFirstName(types=types, route="change_first_name", link_route="change_name")
    if await sr.get_client_data():
        await show_settings(types=types)
    return None


async def change_last_name(types):
    sr = ChangeLastName(types=types, route="change_last_name", link_route="change_name")
    if await sr.get_client_data():
        await show_settings(types=types)
    return None


async def change_max_access_limit(types):
    sr = ChangeMaxAccessLimit(types=types, route="change_max_access_limit", link_route="show_settings")
    if await sr.get_client_data():
        await show_settings(types=types)
    return None


async def change_password(types):
    sr = ChangePassword(types=types, route="change_password", link_route="show_settings")
    if await sr.get_client_data():
        await main(types=types) if CLIENT_INFO[types.from_user.id].result else await show_settings(types=types)
    return None


async def change_visibility(types):
    sr = ChangeVisibility(types=types, route="change_visibility", link_route="show_settings")
    if await sr.get_client_data():
        await show_settings(types=types)
    return None


async def delete_kryptos(types):
    sr = DeleteKryptos(types=types, route="delete_kryptos", link_route="settings")
    if await sr.get_client_data():
        if CLIENT_INFO[types.from_user.id].result:
            CLIENT_INFO.pop(types.from_user.id)
            await main(types=types)

        else:
            await settings(types=types)

    return None


async def license_settings(types):
    sr = LicenseSettings(types=types, route="license_settings")
    await sr.send_message()
    return None


async def register_license(types):
    sr = RegisterLicense(types=types, route="register_license", link_route="settings")
    if await sr.get_uploaded_file():
        await license_settings(types=types)
    return None


async def show_settings(types):
    sr = ShowCurrentSettings(types=types, route="settings", link_route="settings")
    await sr.send_message()
    return None


async def settings(types):
    if await check_signin(types=types):
        sr = Settings(types=types, route="settings")
        await sr.send_message()
        return None

    await main(types=types)
    return None
