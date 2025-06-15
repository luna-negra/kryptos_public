from mizuhara.core.routes import (connector_callback,
                                  connector_command,
                                  connector_message,)

from settings.views import *


# Mapping handlers and views for Telegram Bot commands.
COMMANDS: list = [
    connector_command(view=settings, commands=["settings"]),
]


MESSAGES: list = [
    connector_message(view=change_max_access_limit, allowed_pre_route=["change_max_access_limit"]),
    connector_message(view=change_first_name, allowed_pre_route=["change_first_name"]),
    connector_message(view=change_last_name, allowed_pre_route=["change_last_name"]),
    connector_message(view=change_password, allowed_pre_route=["change_password"]),
    connector_message(view=change_visibility, allowed_pre_route=["change_visibility"]),
    connector_message(view=register_license, content_types=["document"], allowed_pre_route=["register_license"]),
    connector_message(view=delete_kryptos, allowed_pre_route="delete_kryptos"),
    connector_message(view=main)
]


CALLBACKS: list = [
    connector_callback(view=change_max_access_limit,
                       callback_data=["change_max_access_limit"],
                       allowed_pre_route=["settings"]),
    connector_callback(view=change_language,
                       callback_data=["change_language", "en", "ja", "ko"],
                       allowed_pre_route=["settings", "change_language"]),
    connector_callback(view=change_last_name,
                       callback_data=["change_last_name"],
                       allowed_pre_route=["change_name"]),
    connector_callback(view=change_first_name,
                       callback_data=["change_first_name"],
                       allowed_pre_route=["change_name"]),
    connector_callback(view=change_password,
                       callback_data=["change_password"],
                       allowed_pre_route=["settings"]),
    connector_callback(view=change_name,
                       callback_data=["change_name"],
                       allowed_pre_route=["settings", "change_first_name", "change_last_name"]),
    connector_callback(view=change_visibility,
                       callback_data=["change_visibility"],
                       allowed_pre_route=["settings"]),
    connector_callback(view=delete_kryptos,
                       callback_data=["delete_kryptos"],
                       allowed_pre_route=["settings"]),
    connector_callback(view=license_settings,
                       callback_data=["license_settings"],
                       allowed_pre_route=["settings"]),
    connector_callback(view=register_license,
                       callback_data=["register_license"],
                       allowed_pre_route=["license_settings"]),
    connector_callback(view=settings,
                       callback_data=["settings"],
                       allowed_pre_route=["settings", "delete_kryptos", "license_settings", "main_member", "register_license"]),
    connector_callback(view=show_settings,
                       callback_data=["show_settings"],
                       allowed_pre_route=["settings", "change_max_access_limit", "change_language", "change_name", "change_password", "change_visibility",]),
    connector_callback(view=main)
]
