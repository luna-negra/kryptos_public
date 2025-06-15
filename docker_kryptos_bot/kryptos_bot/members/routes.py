from mizuhara.core.routes import (connector_callback,
                                  connector_command,
                                  connector_message,)
from members.views import *


# Mapping handlers and views for Telegram Bot commands.
COMMANDS: list = [
    connector_command(view=main, commands=["start", "main"]),
]


MESSAGES: list = [
    connector_message(view=activate_account, allowed_pre_route=["activation"], regexp="^[A-z0-9=]"),
    connector_message(view=signin, allowed_pre_route=["signin"]),
    connector_message(view=signup, allowed_pre_route=["signup"]),
]

CALLBACKS: list = [
    connector_callback(view=activation, callback_data=["activation"], allowed_pre_route=["activation"]),
    connector_callback(view=activate_account, callback_data=["input_code", "send_code"], allowed_pre_route=["activation"]),
    connector_callback(view=main, callback_data=["main"], allowed_pre_route=["management", "settings"]),
    connector_callback(view=main_anon, callback_data=["main_anon"]),
    connector_callback(view=signin, callback_data=["signin"], allowed_pre_route=["main_anon"]),
    connector_callback(view=signout, callback_data=["signout"]),
    connector_callback(view=signup, callback_data=["signup"], allowed_pre_route=["main_anon"])
]
