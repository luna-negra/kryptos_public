import asyncio, requests, io, yaml

from os import getenv
from pyzipper import (is_zipfile,
                      AESZipFile,)
from telebot.async_telebot import AsyncTeleBot
from telebot.types import (ForceReply,
                           InlineKeyboardButton,)
from telebot.util import quick_markup

from kryptos_bot_tools.language_pack import *
from tools.regex import (regex_match,
                         regex_search,
                         REGEX_EMAIL,
                         REGEX_PASSWORD_LOWER,
                         REGEX_PASSWORD_UPPER,
                         REGEX_PASSWORD_SPECIAL,
                         REGEX_PASSWORD_DIGIT,
                         REGEX_URL_BODY,
                         REGEX_UUID,)


# Start Async TeleBot Object
bot = AsyncTeleBot(token= getenv("KRYPTOS_BOT_API_TOKEN"))

# Options
DEFAULT_LANGUAGE_CODE = "en"
LANGUAGE_CODE_LIST:dict = {"en": "🇬🇧 English",  "ja": "🇯🇵 日本語", "ko": "🇰🇷 한국어"}
MESSENGER_CODE = "TLGR"
URL_ROOT: str = "http://{}:8000/api/v1{}".format(getenv("KRYPTOS_API_HOST_IP"), "{}")
TIMEOUT: int = int(getenv("KRYPTOS_BOT_API_TIMEOUT") or 10)

# user_action_tracking
USER_STATUS: dict = {}
USER_ACTION: dict = {}
USER_DATA: dict = {}
USER_INFO: dict = {}
USER_LANGUAGE: dict = {}


@bot.callback_query_handler(func=lambda cb: cb.data == "anon_main")
async def anon_main(msg=None, cb=None) -> None:
    request_user = msg.from_user if cb is None else cb.from_user
    chat_id: int = request_user.id
    user_name: str = f"{request_user.first_name}"
    language_code: str = request_user.language_code if request_user.language_code in LANGUAGE_CODE_LIST else DEFAULT_LANGUAGE_CODE

    # update user information
    USER_STATUS.update({chat_id: "anon_main"})
    USER_ACTION.update({chat_id: "start"})
    USER_LANGUAGE.update({chat_id: language_code})
    USER_DATA[chat_id] = {"chat_info": {"msg_name": MESSENGER_CODE, "chat_id": str(chat_id), "is_signed_in": True}}

    # prepare text and markup
    prompt: dict = PROMPT_START.get(USER_LANGUAGE[chat_id])
    prompt_btn: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])
    text = prompt.get("intro").format(user_name) + prompt.get("welcome")
    markup = quick_markup({})
    markup.add(InlineKeyboardButton(text=prompt_btn.get("signin_btn"), callback_data="signin"),
               InlineKeyboardButton(text=prompt_btn.get("signup_btn"), callback_data="signup"))

    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


async def activate(chat_id) -> None:
    chat_id: int = chat_id #request_user.id
    prompt: dict = PROMPT_ACTIVATE.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_STATUS.update({chat_id: "activate"})

    # prepare text and markup
    text = prompt.get("intro")
    markup = quick_markup({})
    markup.add(InlineKeyboardButton(text=prompt_button.get("send_code_btn"), callback_data="api_send_code"),
               InlineKeyboardButton(text=prompt_button.get("skip_btn"), callback_data="activate"),
               InlineKeyboardButton(text=prompt_button.get("signout_btn"), callback_data="signout"))

    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "change_pw" and USER_STATUS.get(cb.from_user.id) == "settings")
async def change_password(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_EDIT_PASSWORD.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "change_pw"})

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="settings"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    await prompt_password(cb=cb)
    return None


@bot.message_handler(content_types=['document'], func=lambda msg: USER_STATUS.get(msg.from_user.id) == "settings" and USER_ACTION.get(msg.from_user.id) == "register_license")
async def check_license_file(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_LICENSE.get(USER_LANGUAGE.get(chat_id))

    file_id = msg.document.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    download_file = await bot.download_file(file_path=file_path)
    zip_file = io.BytesIO(download_file)

    # remove user message with uploading file
    await bot.delete_message(chat_id=chat_id, message_id=msg.id)

    # validate license file
    flag = False

    if is_zipfile(filename=zip_file):
        try:
            with AESZipFile(file=zip_file, mode="r") as zip_ref:
                zip_ref.setpassword(getenv("KRYPTOS_BOT_CODEBOOK").encode())
                inner_file_list: list = zip_ref.namelist()

                if len(inner_file_list) == 1:
                    with zip_ref.open(inner_file_list[0], mode="r") as f:
                        contents: dict = yaml.safe_load(f.read().decode("utf-8"))

                    # Important to forking.
                    flag = True

        except (RuntimeError, yaml.YAMLError,) as e:
            pass

    if flag:
        await api_register_license(msg=msg, contents=contents)

    else:
        await bot.send_message(chat_id=chat_id, text=prompt.get("invalid"))
        await settings(msg=msg)

    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "create_new_doc" and USER_STATUS.get(cb.from_user.id) in ("docs",))
async def create_new_doc(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_CREATE_DOC.get(USER_LANGUAGE.get(chat_id))
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE.get(chat_id))

    # update user information
    USER_STATUS.update({chat_id: "create_new_doc"})
    USER_ACTION.update({chat_id: "create_new_doc"})
    USER_DATA[chat_id] = {"chat_info": {"msg_name": MESSENGER_CODE, "chat_id": str(chat_id), "is_signed_in": True}}

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="docs"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    await prompt_doc_site(cb=cb)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "delete_kryptos" and USER_STATUS.get(cb.from_user.id) == "settings")
async def delete_kryptos(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_DELETE_KRYPTOS.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_STATUS.update({chat_id: "delete_kryptos"})

    # prepare text and markup
    text = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("yes_btn"), callback_data="password"),
               InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="settings"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data.startswith("delete_doc_") and USER_STATUS.get(cb.from_user.id) == "search_docs")
async def delete_doc(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id

    # update user information
    USER_STATUS.update({chat_id: "delete_doc"})
    USER_ACTION.update({chat_id: "start"})
    await final_check_delete_doc(cb=cb)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "docs" and USER_STATUS.get(cb.from_user.id) in ("member_main", "docs", "create_new_doc", "search_docs",))
async def docs(msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: str = PROMPT_DOCS.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_STATUS.update({chat_id: "docs"})
    USER_ACTION.update({chat_id: "start"})
    USER_DATA[chat_id] = {"chat_info": {"msg_name": MESSENGER_CODE, "chat_id": str(chat_id), "is_signed_in": True}}

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("create_new_doc"), callback_data="create_new_doc"))
    markup.add(InlineKeyboardButton(text=prompt_button.get("search_docs"), callback_data="search_docs"))
    markup.add(InlineKeyboardButton(text=prompt_button.get("statistics_docs"), callback_data="statistics_docs"))
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="member_main"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


async def is_account_active(msg=None, cb=None) -> bool: #chat_id) -> bool:
    #data: dict = await api_get_user_info(chat_id=chat_id)
    data: dict = await api_get_user_info(msg=msg, cb=cb)
    return  data.get("is_active", False)


@bot.callback_query_handler(func=lambda cb: cb.data == "edit_language" and USER_STATUS.get(cb.from_user.id) == "settings")
async def edit_language(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_EDIT_LANGUAGE.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "language"})

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = quick_markup(values={}, row_width=3)
    markup.add(InlineKeyboardButton(text=LANGUAGE_CODE_LIST.get("en"), callback_data="language_en"),
               InlineKeyboardButton(text=LANGUAGE_CODE_LIST.get("ja"), callback_data="language_ja"))
    markup.add(InlineKeyboardButton(text=LANGUAGE_CODE_LIST.get("ko"), callback_data="language_ko"),
               InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="settings"))

    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "edit_name" and USER_STATUS.get(cb.from_user.id) == "settings")
async def edit_name(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_EDIT_NAME.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "name"})

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("edit_first_name_btn"), callback_data="first_name"),
               InlineKeyboardButton(text=prompt_button.get("edit_last_name_btn"), callback_data="last_name"))
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="settings"))

    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "edit_max_access" and USER_STATUS.get(cb.from_user.id) == "settings")
async def edit_max_access(cb):
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_EDIT_MAX_ACCESS.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "max_access"})

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="settings"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    await prompt_max_access(cb=cb)


@bot.callback_query_handler(func=lambda cb: cb.data.startswith("language_") and USER_STATUS.get(cb.from_user.id) == "settings")
async def edit_language(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    language: str = cb.data.split("_")[1]

    # update user information
    USER_DATA[chat_id].update({"language": language})

    await api_update_account(cb=cb)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "edit_visibility" and USER_STATUS.get(cb.from_user.id) == "settings")
async def edit_visibility(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_EDIT_VISIBILITY.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "visibility"})

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="settings"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    await prompt_visibility(cb=cb)
    return None


async def final_check_delete_doc(cb):
    request_user = cb.from_user
    chat_id: int = request_user.id
    doc_uuid: str = cb.data.replace("delete_doc_", "")
    prompt: dict = PROMPT_CHECK_DELETE_DOC.get(USER_LANGUAGE.get(chat_id))
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE.get(chat_id))

    # update user information
    USER_ACTION.update({chat_id: "check_delete_doc"})

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("yes_btn"), callback_data=f"api_delete_doc_{doc_uuid}"),
               InlineKeyboardButton(text=prompt_button.get("no_btn"), callback_data=doc_uuid))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


async def final_check_signup(msg) -> None:
    chat_id: int = msg.chat.id
    prompt: dict = PROMPT_CHECK_SIGNUP.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "final_check_signup"})
    USER_DATA[chat_id].update({"first_name": msg.from_user.first_name,
                               "last_name": msg.from_user.last_name,
                               "language": USER_LANGUAGE[chat_id]})
    USER_DATA[chat_id]["chat_info"].update({"is_signed_in": False})

    # prepare markup and text
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("yes_btn"), callback_data="api_siginup"),
               InlineKeyboardButton(text=prompt_button.get("no_btn"), callback_data="anon_main"))

    text = f"""[ {prompt.get("intro")} ]

*  {prompt.get("email")}: {USER_DATA[chat_id].get("email")}

{prompt.get("final_check")}
    """

    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: regex_match(pattern=REGEX_UUID, string=cb.data) is not None)
async def get_doc(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id

    # update user info
    USER_STATUS.update({chat_id: "search_docs"})
    USER_ACTION.update({chat_id: "get_doc"})

    await api_get_doc_info(cb=cb)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "get_license" and USER_ACTION.get(cb.from_user.id) == "license")
async def get_license(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_LICENSE.get(USER_LANGUAGE.get(chat_id))
    prompt_btn: dict = PROMPT_BUTTON.get(USER_LANGUAGE.get(chat_id))

    #prepare text and markup
    license_data = USER_INFO.get(chat_id).get("license_info")

    if license_data != {}:
        text: str = f"""{prompt.get("show_intro")}
    
* {prompt.get("max_number_account")}: {license_data.get("kryptos_license").get("documents")}
* {prompt.get("license_expire")}: {license_data.get("kryptos_license_issued")}    
* {prompt.get("license_issue")}: {license_data.get("kryptos_license_expire")}
    """

    else:
        text: str = prompt.get("no_license")

    await bot.send_message(chat_id=chat_id, text=text)

    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_btn.get("skip_btn"), callback_data="license"))
    await bot.send_message(chat_id=chat_id, text=prompt.get("continue"), reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "license" and USER_STATUS.get(cb.from_user.id) == "settings")
async def license(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_LICENSE.get(USER_LANGUAGE.get(chat_id))
    prompt_btn: dict = PROMPT_BUTTON.get(USER_LANGUAGE.get(chat_id))

    # update user info
    USER_ACTION.update({chat_id: "license"})

    # prepare text and
    text: str = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_btn.get("get_license_btn"), callback_data="get_license"),
               InlineKeyboardButton(text=prompt_btn.get("register_license_btn"), callback_data="register_license"))
    markup.add(InlineKeyboardButton(text=prompt_btn.get("cancel_btn"), callback_data="settings"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "member_main")
async def member_main(cb=None, msg=None) -> None:
    request_user = msg.from_user if cb is None else cb.from_user
    chat_id: int = request_user.id

    # update user information
    USER_STATUS.update({chat_id: "member_main"})
    USER_ACTION.update({chat_id: "start"})
    USER_DATA[chat_id] = {"chat_info": {"msg_name": MESSENGER_CODE, "chat_id": str(chat_id), "is_signed_in": True}}

    # check active
    is_active: bool = await is_account_active(msg=msg, cb=cb)

    # update user information
    USER_LANGUAGE.update({chat_id: USER_INFO[chat_id].get("language") if USER_INFO.get(chat_id, None) is not None else request_user.language_code})

    # set additional variables
    prompt: dict = PROMPT_START.get(USER_LANGUAGE.get(chat_id))
    prompt_btn: dict = PROMPT_BUTTON.get(USER_LANGUAGE.get(chat_id))

    if not is_active:
        text = prompt.get("activate_warning")
        await bot.send_message(chat_id=chat_id, text=text)
        await activate(chat_id=chat_id)

    else:
        # get username
        user_name: str = USER_INFO[chat_id].get('first_name')

        # prepare text and markup
        text = prompt.get("intro").format(user_name) + prompt.get("serve_member")
        markup = quick_markup({})
        markup.add(InlineKeyboardButton(text=prompt_btn.get("account_btn"), callback_data="docs"))
        markup.add(InlineKeyboardButton(text=prompt_btn.get("setting_btn"), callback_data="settings"),
                   InlineKeyboardButton(text=prompt_btn.get("signout_btn"), callback_data="signout"))

        await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
        return None


@bot.callback_query_handler(func=lambda cb: cb.data in ("first_name", "last_name", ) and USER_STATUS.get(cb.from_user.id) == "settings")
async def name(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_EDIT_NAME.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: cb.data})
    await prompt_name(cb=cb)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "register_license" and USER_ACTION.get(cb.from_user.id) == "license")
async def register_license(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_LICENSE.get(USER_LANGUAGE.get(chat_id))
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE.get(chat_id))

    # update user info
    USER_ACTION.update({chat_id: "register_license"})

    # prepare text and markup
    text: str = prompt.get("register_intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="license"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "search_docs" and USER_STATUS.get(cb.from_user.id) in ("docs", "search_docs", "create_new_doc", "update_doc", "delete_doc"))
async def search_docs(cb=None, msg=None):
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_SEARCH_DOCS.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user info
    USER_STATUS.update({chat_id: "search_docs"})
    USER_ACTION.update({chat_id: "start"})
    USER_DATA[chat_id] = {"chat_info": {"msg_name": MESSENGER_CODE, "chat_id": str(chat_id), "is_signed_in": True}}

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("search_docs_site"), callback_data="search_docs_site"))
    markup.add(InlineKeyboardButton(text=prompt_button.get("search_docs_description"), callback_data="search_docs_description"))
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="docs"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "settings" and USER_STATUS.get(cb.from_user.id) in ("member_main", "settings", "delete_kryptos"))
async def settings(cb=None, msg=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_SETTING.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_STATUS.update({chat_id: "settings"})
    USER_ACTION.update({chat_id: "start"})
    USER_DATA[chat_id] = {"chat_info": {"msg_name": MESSENGER_CODE, "chat_id": str(chat_id), "is_signed_in": True}}

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("show_settings_btn"), callback_data="show_settings"),
               InlineKeyboardButton(text=prompt_button.get("edit_name_btn"), callback_data="edit_name"),)
    markup.add(InlineKeyboardButton(text=prompt_button.get("edit_language_btn"), callback_data="edit_language"),
               InlineKeyboardButton(text=prompt_button.get("edit_max_access_btn"), callback_data="edit_max_access"),)
    markup.add(InlineKeyboardButton(text=prompt_button.get("edit_visibility_btn"), callback_data="edit_visibility"),
               InlineKeyboardButton(text=prompt_button.get("edit_password_btn"), callback_data="change_pw"),)
    markup.add(InlineKeyboardButton(text=prompt_button.get("license_btn"), callback_data="license"),
               InlineKeyboardButton(text=prompt_button.get("delete_kryptos_btn"), callback_data="delete_kryptos"),)
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="member_main"),)

    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data.startswith("search_docs_") and USER_STATUS.get(cb.from_user.id) in ("search_docs",))
async def search_docs_intro(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_SEARCH_DOCS.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])
    callback_data: str = cb.data

    # update user information
    USER_ACTION.update({chat_id: "search_docs_site" if callback_data == "search_docs_site" else "search_docs_description"} )

    # prepare text and markup
    text: str = prompt.get("intro_url") if callback_data == "search_docs_site" else prompt.get("intro_description")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="search_docs"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    await prompt_doc_site(cb=cb) if callback_data == "search_docs_site" else await prompt_doc_description(cb=cb)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "show_settings" and USER_STATUS.get(cb.from_user.id) == "settings")
async def show_settings(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_SETTING.get(USER_LANGUAGE[chat_id])

    # update for user
    USER_ACTION.update({chat_id: "show_settings"})

    # prepare text and markup
    text: str = prompt.get("show_intro")
    await bot.send_message(chat_id=chat_id, text=text)

    data: dict = USER_INFO[chat_id]
    text: str = f"""
* {prompt.get("email")}: {data.get("email")}
* {prompt.get("first_name")}: {data.get("first_name")}
* {prompt.get("last_name")}: {data.get("last_name")}
* {prompt.get("language")}: {LANGUAGE_CODE_LIST.get(data.get("language"))}
* {prompt.get("max_access_try")}: {data.get("max_access_try")}
* {prompt.get("visibility")}: {data.get("visibility")} % 
* {prompt.get("last_signin_datetime")}: {data.get("last_access_datetime").replace("T", " ").split(".")[0]}
* {prompt.get("last_signout_datetime")}: {data.get("last_signout_datetime").replace("T", " ").split(".")[0]}
* {prompt.get("last_updated_datetime")}: {data.get("last_updated_datetime").replace("T", " ").split(".")[0]}
* {prompt.get("registered_datetime")}: {data.get("registered_datetime").replace("T", " ").split(".")[0]}
"""
    await bot.send_message(chat_id=chat_id, text=text)
    await settings(cb=cb)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "signin" and USER_STATUS.get(cb.from_user.id) in ("anon_main", "signin", "signup"))
async def signin(cb=None, msg=None) -> None:
    request_user = cb.from_user if cb is not None else msg.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_SIGNIN.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_STATUS.update({chat_id: "signin"})
    USER_ACTION.update({chat_id: "start"})

    # prepare markup and text
    text = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="anon_main"))

    # execute prompt to get email
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    await prompt_email(chat_id)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "signout")
async def signout(cb) -> None:
    await api_signout(cb)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "signup" and USER_STATUS.get(cb.from_user.id) in ("anon_main", "signin", "signup"))
async def signup(cb=None, msg=None) -> None:
    request_user = cb.from_user if cb is not None else msg.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_SIGNUP.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_STATUS.update({chat_id: "signup"})
    USER_ACTION.update({chat_id: "start"})

    # prepare markup and text
    text = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="anon_main"))

    # execute prompt to get email
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    await prompt_email(chat_id)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "statistics_docs" and USER_STATUS.get(cb.from_user.id) in ("docs",))
async def statistics_docs(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    await api_get_doc_statistics(cb)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data.startswith("update_doc_") and USER_STATUS.get(cb.from_user.id) in ("search_docs", ))
async def update_doc(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    doc_uuid: str = cb.data.split("_")[2]
    prompt: dict = PROMPT_UPDATE_DOC.get(USER_LANGUAGE.get(chat_id))
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE.get(chat_id))

    # update user information
    USER_STATUS.update({chat_id: "update_doc"})
    USER_ACTION.update({chat_id: "update_doc"})
    USER_DATA[chat_id] = {"chat_info": {"msg_name": MESSENGER_CODE, "chat_id": str(chat_id), "is_signed_in": True}, "doc_uuid": doc_uuid}

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("update_site_btn"), callback_data="update_site"),
               InlineKeyboardButton(text=prompt_button.get("update_protocol_btn"), callback_data="update_docs_protocol"))
    markup.add(InlineKeyboardButton(text=prompt_button.get("update_username_btn"), callback_data="update_doc_username"),
               InlineKeyboardButton(text=prompt_button.get("update_password_btn"), callback_data="update_docs_password"))
    markup.add(InlineKeyboardButton(text=prompt_button.get("update_description_btn"), callback_data="update_docs_description"),
               InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data=doc_uuid),)
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "activate" and USER_STATUS.get(cb.from_user.id) == "activate")
async def prompt_activate(cb=None, msg=None) -> None:
    request_user = msg.from_user if cb is None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_ACTIVATE.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "input_code"})

    # prepare text and markup
    text: str = prompt.get("guide")
    markup = ForceReply(input_field_placeholder=prompt.get("placeholder"))

    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda cb: cb.data in ("update_docs_description", ) and USER_STATUS.get(cb.from_user.id) in ("update_doc",))
async def prompt_doc_description(cb=None, msg=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_DOCS_DESCRIPTION.get(USER_LANGUAGE[chat_id])
    user_status: str = USER_STATUS.get(chat_id)

    # update user information
    USER_ACTION.update({chat_id: "description"})

    # prepare text and markup
    text: str = prompt.get("intro") + (prompt.get("guide") if user_status == "create_new_doc" else "")
    markup = ForceReply(input_field_placeholder=prompt.get("placeholder"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data in ("update_docs_password", ) and USER_STATUS.get(cb.from_user.id) in ("update_doc",))
async def prompt_doc_password(cb=None, msg=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_DOC_PASSWORD.get(USER_LANGUAGE.get(chat_id))

    # update user information
    USER_ACTION.update({chat_id: "doc_password"})

    # prepare text and markup
    text: str = prompt.get("intro") + prompt.get("guide")
    markup = ForceReply(input_field_placeholder=prompt.get("placeholder"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


async def prompt_doc_new_password(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_DOC_NEW_PASSWORD.get(USER_LANGUAGE.get(chat_id))

    # update user information
    USER_ACTION.update({chat_id: "doc_new_password"})

    # prepare text and markup
    text: str = prompt.get("intro")
    markup = ForceReply(input_field_placeholder=prompt.get("placeholder"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "update_docs_protocol" and USER_STATUS.get(cb.from_user.id) in ("update_doc",))
async def prompt_doc_protocol(cb=None, msg=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_DOC_PROTOCOL.get(USER_LANGUAGE.get(chat_id))
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE.get(chat_id))

    # update user information
    USER_ACTION.update({chat_id: "protocol"})

    # prepare text and markup
    text: str = prompt.get("intro") + prompt.get("guide")
    markup = quick_markup(values={})
    markup.add(InlineKeyboardButton(text=prompt_button.get("pt_https_btn"), callback_data="protocol_https"),
               InlineKeyboardButton(text=prompt_button.get("pt_http_btn"), callback_data="protocol_http"))
    markup.add(InlineKeyboardButton(text=prompt_button.get("pt_ssh_btn"), callback_data=f"protocol_ssh"),
               InlineKeyboardButton(text=prompt_button.get("pt_ftp_btn"), callback_data="protocol_ftp"))
    markup.add(InlineKeyboardButton(text=prompt_button.get("pt_jdbc_btn"), callback_data="protocol_jdbc"),
               InlineKeyboardButton(text=prompt_button.get("pt_srv_btn"), callback_data="protocol_srv"))
    markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="docs"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb:cb.data in ("update_doc_username",) and USER_STATUS.get(cb.from_user.id) in ("update_doc", ))
async def prompt_doc_username(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_DOC_USERNAME.get(USER_LANGUAGE.get(chat_id))

    # update user information
    USER_ACTION.update({chat_id: "username"})

    # prepare text and markup
    text: str = prompt.get("intro") + prompt.get("guide")
    markup = ForceReply()
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: USER_ACTION.get(cb.from_user.id) in ("search_docs_site", "create_new_doc", "update_doc") and USER_STATUS.get(cb.from_user.id) in ("search_docs", "create_new_doc", "update_doc"))
async def prompt_doc_site(cb=None, msg=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_DOC_SITE.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "site"})

    # prepare text and markup
    text: str = prompt.get("intro") + (prompt.get("guide") if USER_STATUS.get(chat_id) == "create_new_doc" else "")
    markup = ForceReply(input_field_placeholder=prompt.get("placeholder"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


async def prompt_email(chat_id) -> None:
    prompt: dict = PROMPT_EMAIL.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "email"})

    # prepare text and markup
    markup = ForceReply(input_field_placeholder=prompt.get("placeholder"))
    text = prompt.get("intro")
    text += prompt.get("add_detail") if USER_STATUS[chat_id] == "signup" else ""

    await bot.send_message(chat_id=chat_id, text=text,reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "edit_max_access" and USER_STATUS.get(cb.from_user.id) == "setting")
async def prompt_max_access(cb=None, msg=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_EDIT_MAX_ACCESS.get(USER_LANGUAGE[chat_id])

    # there is no update for user

    # prepare text and markup
    text: str = prompt.get("guide")
    markup = ForceReply(input_field_placeholder=prompt.get("placeholder"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


async def prompt_name(msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_EDIT_NAME.get(USER_LANGUAGE[chat_id])

    # there is no user update

    # prepare text and markup
    text: str = prompt.get(cb.data)
    markup = ForceReply(input_field_placeholder=prompt.get("placeholder"))

    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "password" and USER_STATUS.get(cb.from_user.id) in ("settings", "delete_kryptos"))
async def prompt_password(msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id = request_user.id
    prompt: dict = PROMPT_PASSWORD.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "password"})

    # prepare text and markup
    text = prompt.get("intro") + "\n"
    markup = ForceReply(input_field_placeholder="Password: ")

    if USER_STATUS[chat_id] in ("signup",):
        text += prompt.get("add_detail")

    if USER_STATUS[chat_id] in ("settings", ):
        text = prompt.get("change_pw")

    await bot.send_message(chat_id=chat_id,
                           text=text,
                           reply_markup=markup)

    return None


async def prompt_new_password(msg) -> None:
    request_user =  msg.from_user
    chat_id = request_user.id
    prompt: dict = PROMPT_PASSWORD.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "new_password"})

    # prepare text and markup
    text = prompt.get("new_password_intro") + prompt.get("add_detail")
    markup = ForceReply()
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


async def prompt_visibility(msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_EDIT_VISIBILITY.get(USER_LANGUAGE[chat_id])

    # there is no user update

    # prepare text and markup
    text: str = prompt.get("guide")
    markup = ForceReply(input_field_placeholder=prompt.get("placeholder"))
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
    return None


@bot.message_handler(func=lambda msg: USER_STATUS.get(msg.from_user.id) == "activate" and USER_ACTION.get(msg.from_user.id) == "input_code")
async def validate_activation_code(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    message_id: int = msg.message_id
    input_code: str = msg.text
    prompt: dict = PROMPT_ACTIVATE.get(USER_LANGUAGE[chat_id])

    # delete user input
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    if len(input_code) != 6:
        text: str = prompt.get("code_invalidate")
        await bot.send_message(chat_id=chat_id, text=text)
        await prompt_activate(msg=msg)

    else:
        await api_activate(msg=msg)

    return None


@bot.message_handler(func=lambda msg: USER_ACTION.get(msg.chat.id) == "description" and USER_STATUS.get(msg.chat.id) in ("create_new_doc", "search_docs", "update_doc",))
async def validate_doc_description(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    input_url: str = msg.text
    message_id: int = msg.message_id
    user_status: str = USER_STATUS.get(msg.chat.id)

    # delete user input
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    # update user information
    USER_DATA[chat_id].update({"description": input_url})

    if user_status == "search_docs":
        await api_search_docs(msg=msg)

    elif user_status == "create_new_doc":
        await api_create_new_doc(msg=msg)

    else:
        await api_update_doc(msg=msg)

    return None


@bot.message_handler(func=lambda msg: USER_ACTION.get(msg.from_user.id) == "doc_new_password" and USER_STATUS.get(msg.from_user.id) in ("update_doc", ))
async def validate_doc_new_password(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    message_id: int = msg.message_id
    input_new_password: str = msg.text
    user_status: str = USER_STATUS.get(chat_id)

    # delete user input
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    # update user information
    USER_DATA[chat_id].update({"new_password": input_new_password})
    await api_change_password_doc(msg=msg)
    return None


@bot.message_handler(func=lambda msg: USER_ACTION.get(msg.from_user.id) == "doc_password" and USER_STATUS.get(msg.from_user.id) in ("create_new_doc", "update_doc", ))
async def validate_doc_password(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    message_id: int = msg.message_id
    input_password: str = msg.text
    user_status: str = USER_STATUS.get(chat_id)

    # delete user input
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    # update user information
    USER_DATA[chat_id].update({"password": input_password})

    if user_status == "create_new_doc":
        await prompt_doc_description(msg=msg)

    else:
        await prompt_doc_new_password(msg=msg)

    return None


@bot.callback_query_handler(func=lambda cb: cb.data.startswith("protocol_") and USER_STATUS.get(cb.from_user.id) in ("create_new_doc", "update_doc"))
async def validate_doc_protocol(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    input_protocol: str = cb.data.split("_")[1]
    user_status : str = USER_STATUS.get(chat_id)

    # update user information
    USER_DATA[chat_id].update({"protocol": input_protocol})

    if user_status == "create_new_doc":
        await prompt_doc_username(cb=cb)

    else:
        await api_update_doc(cb=cb)

    return None


@bot.message_handler(func=lambda msg: USER_ACTION.get(msg.chat.id) == "username" and USER_STATUS.get(msg.chat.id) in ("create_new_doc", "update_doc"))
async def validate_doc_username(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    input_username: str = msg.text
    message_id: int = msg.message_id
    prompt: dict = PROMPT_DOC_USERNAME.get(USER_LANGUAGE.get(chat_id))
    user_status: str = USER_STATUS.get(chat_id)

    # delete user input
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    USER_DATA[chat_id].update({"username": input_username})

    if user_status == "create_new_doc":
        await prompt_doc_password(msg=msg)

    else:
        await api_update_doc(msg=msg)

    return None


@bot.message_handler(func=lambda msg: USER_ACTION.get(msg.chat.id) == "site" and USER_STATUS.get(msg.chat.id) in ("search_docs", "create_new_doc", "update_doc"))
async def validate_doc_site(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    input_url: str = msg.text.lower()
    message_id: int = msg.message_id
    prompt: dict = PROMPT_DOC_SITE.get(USER_LANGUAGE.get(chat_id))
    user_status: str = USER_STATUS.get(chat_id)

    # delete user input
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    if not regex_search(pattern=REGEX_URL_BODY, string=input_url):
        text: str = prompt.get("fail")
        await bot.send_message(chat_id=chat_id, text=text)
        await prompt_doc_site(msg=msg)

    else:
        # update user information
        USER_DATA[chat_id].update({"site": input_url})

        if user_status == "search_docs":
            await api_search_docs(msg=msg)

        elif user_status == "create_new_doc":
            await prompt_doc_protocol(msg=msg)

        else:
            await api_update_doc(msg=msg)

    return None


@bot.message_handler(func=lambda msg: USER_ACTION.get(msg.chat.id, None) == "email" and USER_STATUS.get(msg.chat.id, None) in ("signin", "signup"))
async def validate_email(msg) -> None:
    email: str = msg.text
    chat_id: int = msg.from_user.id
    message_id: int = msg.message_id
    prompt: dict = PROMPT_EMAIL.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "validate_email"})

    # check the user input as an email format.
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    if not regex_match(pattern=REGEX_EMAIL, string=email):
        text = prompt.get("invalid")
        await bot.send_message(chat_id=chat_id, text=text)
        await prompt_email(chat_id)

    else:
        USER_DATA[chat_id].update({"email": email})
        await prompt_password(msg=msg)

    return None


@bot.message_handler(func=lambda msg: USER_ACTION.get(msg.from_user.id) in ("first_name", "last_name", ) and USER_STATUS.get(msg.from_user.id) == "settings")
async def validate_name(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    input_name: str = msg.text[0].upper() + msg.text[1:]
    prompt: dict = PROMPT_EDIT_NAME.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])
    field_list: tuple = ("last_name", "first_name")

    # update user information
    USER_DATA[chat_id].update({USER_ACTION[chat_id]: input_name})

    for field in field_list:
        if field not in USER_DATA[chat_id]:
            text: str = prompt.get(f"edit_{field}_question")
            markup = quick_markup(values={})
            markup.add(InlineKeyboardButton(text=prompt_button.get("yes_btn"), callback_data=field),
                       InlineKeyboardButton(text=prompt_button.get("no_btn"), callback_data="api_update_account"))
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
            return None

    await api_update_account(msg=msg)
    return None


@bot.message_handler(func=lambda msg: USER_ACTION.get(msg.chat.id) == "max_access" and USER_STATUS.get(msg.from_user.id) == "settings")
async def validate_max_access(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    message_id: int = msg.message_id
    input_max_access: str = msg.text
    prompt: dict = PROMPT_EDIT_MAX_ACCESS.get(USER_LANGUAGE[chat_id])

    # there is no user update

    # delete message
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    # prepare text and markup
    if input_max_access in ("3", "4", "5"):
        USER_DATA[chat_id].update({"max_access_try": int(input_max_access)})
        await api_update_account(msg=msg)

    else:
        text: str = prompt.get("invalid_value")
        await bot.send_message(chat_id=chat_id, text=text)
        await prompt_max_access(msg=msg)

    return None


@bot.message_handler(func=lambda msg: USER_ACTION.get(msg.chat.id) == "new_password" and USER_STATUS.get(msg.chat.id) == "settings")
async def validate_new_password(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    message_id: int = msg.message_id
    new_password: str = msg.text
    prompt: dict = PROMPT_PASSWORD.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "validate_new_password"})

    # password validation and set text
    text = ""

    if USER_STATUS[chat_id] in ("signup",):
        text += "" if regex_search(pattern=REGEX_PASSWORD_LOWER, string=new_password) else prompt.get("invalid_lower")
        text += "" if regex_search(pattern=REGEX_PASSWORD_UPPER, string=new_password) else prompt.get("invalid_upper")
        text += "" if regex_search(pattern=REGEX_PASSWORD_SPECIAL, string=new_password) else prompt.get("invalid_special")
        text += "" if regex_search(pattern=REGEX_PASSWORD_DIGIT, string=new_password) else prompt.get("invalid_digit")
        text += "" if len(new_password) >= 8 else prompt.get("invalid_length")

        # delete user input
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    if text == "":
        USER_DATA[chat_id].update({"new_password": new_password})
        await api_change_password(msg=msg)

    else:
        await bot.send_message(chat_id=chat_id, text=text)
        await prompt_new_password(msg)

    return None
    

@bot.message_handler(func=lambda msg: USER_ACTION.get(msg.chat.id) == "password" and USER_STATUS.get(msg.chat.id) in ("signin", "signup", "delete_kryptos", "settings"))
async def validate_password(msg) -> None:
    password: str = msg.text
    chat_id: int = msg.chat.id
    message_id: int = msg.message_id
    user_status: str= USER_STATUS[chat_id]
    prompt: dict = PROMPT_PASSWORD.get(USER_LANGUAGE[chat_id])

    # there is no user update

    # password validation and set text
    text = ""

    if USER_STATUS[chat_id] in ("signup",):
        text += "" if regex_search(pattern=REGEX_PASSWORD_LOWER, string=password) else prompt.get("invalid_lower")
        text += "" if regex_search(pattern=REGEX_PASSWORD_UPPER, string=password) else prompt.get("invalid_upper")
        text += "" if regex_search(pattern=REGEX_PASSWORD_SPECIAL, string=password) else prompt.get("invalid_special")
        text += "" if regex_search(pattern=REGEX_PASSWORD_DIGIT, string=password) else prompt.get("invalid_digit")
        text += "" if len(password) >= 8 else prompt.get("invalid_length")

    # delete user input
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    if text == "":
        USER_DATA[chat_id].update({"password": password})

        if user_status == "signin":
            await api_signin(msg=msg)

        elif user_status == "signup":
            await final_check_signup(msg=msg)

        elif user_status == "delete_kryptos":
            await api_delete_kryptos(msg=msg)

        elif user_status == "settings":
            await prompt_new_password(msg=msg)

    else:
        if USER_STATUS[chat_id] == "signup":
            await bot.send_message(chat_id=chat_id, text=text)

        await prompt_password(msg)

    return None


@bot.message_handler(func=lambda msg: USER_ACTION.get(msg.from_user.id) == "visibility" and USER_STATUS.get(msg.from_user.id) == "settings")
async def validate_visibility(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    message_id: int = msg.message_id
    input_visibility: str = msg.text
    prompt: dict = PROMPT_EDIT_VISIBILITY.get(USER_LANGUAGE[chat_id])

    # there is no user update

    # delete message
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

    try:
        if 20 <= int(input_visibility) <=80:
            USER_DATA[chat_id].update({"visibility": input_visibility})
            await api_update_account(msg=msg)
            return None

    except ValueError:
        pass

    # prepare text and markup
    text: str = prompt.get("invalid_value")
    await bot.send_message(chat_id=chat_id, text=text)
    await prompt_visibility(msg=msg)
    return None


@bot.message_handler(func=lambda msg: USER_STATUS.get(msg.from_user.id) == "activate" and USER_ACTION.get(msg.from_user.id) == "input_code")
async def api_activate(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    activation_code: str = msg.text
    api_url: str = URL_ROOT.format("/accounts/activate/")

    # user information update
    USER_DATA[chat_id].update({"activation_code": activation_code})
    USER_ACTION.update({chat_id: "api_activate"})

    # send_api
    try:
        response = requests.put(url=api_url, json=USER_DATA[chat_id], timeout=TIMEOUT)

    except requests.exceptions.ConnectionError:
        await error_api_connection(msg=msg)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(msg=msg)
        return None

    await debrief_api_activate(msg=msg, response=response)
    return None


async def api_create_new_doc(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    api_url: str = URL_ROOT.format("/documents/create/")

    try:
        response = requests.post(url=api_url, json=USER_DATA.get(chat_id), timeout=TIMEOUT)

    except requests.exceptions.ConnectionError:
        await error_api_connection(msg=msg)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(msg=msg)
        return None

    await debrief_api_create_new_doc(msg=msg, response=response)
    return None


@bot.callback_query_handler(func=lambda msg: USER_ACTION.get(msg.from_user.id) == "delete_kryptos" and USER_STATUS.get(msg.from_user.id) == "settings")
async def api_delete_kryptos(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    api_url: str = URL_ROOT.format("/accounts/delete/")

    try:
        response = requests.delete(url=api_url, json=USER_DATA[chat_id], timeout=TIMEOUT)

    except requests.exceptions.ConnectionError:
        await error_api_connection(msg=msg)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(msg=msg)
        return None

    await debrief_api_delete_kryptos(msg=msg, response=response)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data.startswith("api_delete_doc_") and USER_STATUS.get(cb.from_user.id) == "delete_doc")
async def api_delete_doc(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    doc_uuid: str = cb.data.replace("api_delete_doc_", "")
    api_url: str = URL_ROOT.format(f"/documents/{doc_uuid}/delete/")

    try:
        response = requests.delete(url=api_url, json=USER_DATA.get(chat_id), timeout=TIMEOUT)

    except requests.exceptions.ConnectionError:
        await error_api_connection(cb=cb)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(cb=cb)
        return None

    await debrief_api_delete_doc(cb=cb, response=response)
    return None


@bot.message_handler(commands=["start", "main"])
async def api_get_chat_infos(msg) -> None:
    api_url = URL_ROOT.format("/accounts/check_chat/")
    request_user = msg.from_user
    chat_id: int = request_user.id
    language_code = request_user.language_code if request_user.language_code in LANGUAGE_CODE_LIST else DEFAULT_LANGUAGE_CODE

    #update user information
    USER_DATA[chat_id] = {"chat_info": {"msg_name": MESSENGER_CODE, "chat_id": str(chat_id), "is_signed_in": True}}
    USER_LANGUAGE.update({chat_id: language_code})

    # API call
    try:
        response = requests.post(url=api_url, json=USER_DATA[chat_id], timeout=TIMEOUT)

    except requests.exceptions.ConnectionError:
        await error_api_connection(msg=msg)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(msg=msg)
        return None

    await debrief_api_get_chat_infos(msg=msg, response=response)
    return None


async def api_get_doc_info(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    doc_uuid: str = cb.data
    api_url: str = URL_ROOT.format(f"/documents/{doc_uuid}/")

    try:
        response = requests.get(url=api_url, json=USER_DATA.get(chat_id), timeout=TIMEOUT)

    except requests.exceptions.ConnectionError:
        await error_api_connection(cb=cb)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(cb=cb)
        return None

    await debrief_api_get_doc_info(cb=cb, response=response)
    return None


async def api_get_doc_statistics(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    api_url: str = URL_ROOT.format(f"/documents/statistics/")

    try:
        response = requests.get(url=api_url, json=USER_DATA.get(chat_id), timeout=TIMEOUT)

    except requests.exceptions.ConnectionError:
        await error_api_connection(cb=cb)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(cb=cb)
        return None

    await debrief_api_get_doc_statistics(cb=cb, response=response)
    return None


async def api_get_user_info(msg=None, cb=None) -> dict | None: #chat_id=None) -> dict | None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    api_url: str = URL_ROOT.format("/accounts/info/")

    # update user information
    USER_DATA[chat_id].pop("is_signed_in", None)

    # api call
    try:
        response = requests.get(url=api_url, json=USER_DATA[chat_id], timeout=TIMEOUT)

    except requests.exceptions.ConnectionError:
        await error_api_connection(msg=msg, cb=cb)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(msg=msg, cb=cb)
        return None

    if response.status_code == 200:
        data: dict = response.json().get("info")

        if data is not None:
            USER_INFO[chat_id] = data
            USER_LANGUAGE[chat_id] = data.get("language")

        return data

    else:
        return response.json().get("errors")


async def api_register_license(msg, contents) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    api_url: str = URL_ROOT.format("/accounts/license/")

    # there is no update user information
    USER_DATA[chat_id].update({"license_info": contents})

    # api call
    response = requests.post(url=api_url, json=USER_DATA[chat_id])
    await debrief_api_register_license(msg=msg, response=response)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "api_send_code" and USER_STATUS.get(cb.from_user.id) == "activate")
async def api_send_code(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    api_url: str = URL_ROOT.format("/accounts/send_code/")
    prompt: dict = PROMPT_API_SENDCODE.get(USER_LANGUAGE[chat_id])

    # api call
    try:
        response = requests.put(url=api_url, json=USER_DATA[chat_id], timeout=TIMEOUT)

    except requests.exceptions.ConnectionError:
        await error_api_connection(cb=cb)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(cb=cb)
        return None

    # prepare text
    if response.status_code == 200:
        text: str = prompt.get("success")
        await bot.send_message(chat_id=chat_id, text=text)
        await prompt_activate(cb=cb)

    else:
        text: str = prompt.get("fail")
        await bot.send_message(chat_id=chat_id, text=text)

    return None


async def api_search_docs(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    api_url: str = URL_ROOT.format("/documents/?")
    chat_info = USER_DATA.get(chat_id).pop("chat_info")

    for k, v in USER_DATA.get(chat_id).items():
        api_url += f"{k}={v}&"

    USER_DATA[chat_id].update({"chat_info": chat_info})

    try:
        response = requests.get(url=api_url[:-1], json=USER_DATA.get(chat_id))

    except requests.exceptions.ConnectionError:
        await error_api_connection(msg=msg)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(msg=msg)
        return None

    await debrief_api_search_docs(msg=msg, response=response)
    return None


@bot.message_handler(func=lambda msg: USER_STATUS.get(msg.from_user.id) == "signin")
async def api_signin(msg=None, cb=None) -> None:
    api_url = URL_ROOT.format("/accounts/signin/")
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id = request_user.id

    # update user information
    USER_ACTION.update({chat_id: "api_call_signin"})
    USER_DATA[chat_id].update({"chat_info": {"msg_name": MESSENGER_CODE, "chat_id": str(chat_id), "is_signed_in": False}})

    # api call
    try:
        response = requests.post(url=api_url, json=USER_DATA[chat_id])

    except requests.exceptions.ConnectionError:
        await error_api_connection(cb=cb)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(cb=cb)
        return None

    await debrief_api_signin(msg=msg, cb=cb, response=response)
    return  None


async def api_signout(cb) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    api_url: str = URL_ROOT.format("/accounts/signout/")

    try:
        response = requests.put(url=api_url, json=USER_DATA[chat_id])

    except requests.exceptions.ConnectionError:
        await error_api_connection(cb=cb)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(cb=cb)
        return None

    await debrief_api_signout(cb=cb, response=response)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "api_siginup")
async def api_signup(cb) -> None:
    api_url: str = URL_ROOT.format("/accounts/signup/")
    chat_id: int = cb.from_user.id

    # update user information
    USER_ACTION.update({chat_id: "api_call_signup"})

    # api call
    try:
        response = requests.post(url=api_url, json=USER_DATA[chat_id])

    except requests.exceptions.ConnectionError:
        await error_api_connection(cb=cb)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(cb=cb)
        return None

    await debrief_api_signup(cb=cb, response=response)
    return None


@bot.callback_query_handler(func=lambda cb: cb.data == "api_update_account" and USER_STATUS.get(cb.from_user.id) == "settings")
async def api_update_account(msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    api_url: str = URL_ROOT.format("/accounts/update/")

    # api call
    try:
        response = requests.patch(url=api_url, json=USER_DATA[chat_id])

    except requests.exceptions.ConnectionError:
        await error_api_connection(msg=msg, cb=cb)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(msg=msg, cb=cb)
        return None

    await debrief_api_update_account(msg=msg, cb=cb, response=response)


async def api_update_doc(msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    doc_uuid: str = USER_DATA.get(chat_id).pop("doc_uuid")
    api_url: str = URL_ROOT.format(f"/documents/{doc_uuid}/update/")

    try:
        response = requests.put(url=api_url, json=USER_DATA.get(chat_id))

    except requests.exceptions.ConnectionError:
        await error_api_connection(msg=msg, cb=cb)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(msg=msg, cb=cb)
        return None

    await debrief_api_update_doc(msg=msg, cb=cb, response=response)
    return None


async def api_change_password(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    api_url: str = URL_ROOT.format("/accounts/change_pw/")

    # update user information
    USER_ACTION.update({chat_id: "api_change_pw"})

    # api call
    try:
        response = requests.post(url=api_url, json=USER_DATA[chat_id])

    except requests.exceptions.ConnectionError:
        await error_api_connection(msg=msg)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(msg=msg)
        return None

    await debrief_api_change_password(msg=msg, response=response)
    return None


async def api_change_password_doc(msg) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    doc_uuid: str = USER_DATA.get(chat_id).pop("doc_uuid")
    api_url: str = URL_ROOT.format(f"/documents/{doc_uuid}/change_pw/")

    try:
        response = requests.put(url=api_url, json=USER_DATA.get(chat_id))

    except requests.exceptions.ConnectionError:
        await error_api_connection(msg=msg)
        return None

    except requests.exceptions.Timeout:
        await error_db_connection(msg=msg)
        return None

    await debrief_api_change_password_doc(msg=msg, response=response)
    return None


async def debrief_api_activate(msg, response) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_ACTIVATE.get(USER_LANGUAGE[chat_id])

    # process with api result.
    if response.status_code == 200:
        text: str = prompt.get("success")
        await bot.send_message(chat_id=chat_id, text=text)
        await member_main(msg=msg)

    else:
        text: str = prompt.get("fail")
        await bot.send_message(chat_id=chat_id, text=text)
        await activate(chat_id=chat_id)

    return None


async def debrief_api_change_password(response, msg) -> None:
    chat_id = msg.from_user.id
    prompt: dict = PROMPT_API_CHANGE_PASSWORD.get(USER_LANGUAGE[chat_id])

    # process with api result.
    if response.status_code == 200:
        text: str = prompt.get("success")
        await bot.send_message(chat_id=chat_id, text=text)
        await anon_main(msg=msg)

    else:
        text: str = prompt.get("fail")
        await bot.send_message(chat_id=chat_id, text=text)
        await prompt_password(msg=msg)

    return None


async def debrief_api_change_password_doc(msg, response) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_CHANGE_PASSWORD_DOC.get(USER_LANGUAGE.get(chat_id))

    # process with api result.
    text: str = prompt.get("success") if response.status_code == 200 else prompt.get("fail")
    await bot.send_message(chat_id=chat_id, text=text)
    await search_docs(msg=msg)
    
    return None


async def debrief_api_create_new_doc(msg, response) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_CREATE_DOC.get(USER_LANGUAGE.get(chat_id))

    # process with api result.
    if response.status_code == 200:
        text: str = prompt.get("success")

    else:
        text: str = prompt.get("fail")
        errors: str = response.json().get("errors").get("non_field_errors")[0]

        if "license has been expired." == errors:
            text += prompt.get("license_expire")

        elif "you reached license limit." == errors:
            text += prompt.get("reach_limit")

        elif "license is not valid." == errors:
            text += prompt.get("license_invalid")

        elif "document is already created." == errors:
            text += prompt.get("duplicate")

    await bot.send_message(chat_id=chat_id, text=text)
    await docs(msg=msg)
    return None


async def debrief_api_delete_kryptos(msg, response) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_DELETE_KRYPTOS.get(USER_LANGUAGE[chat_id])

    # process with api result.
    if response.status_code == 200:
        # update user info
        USER_DATA.pop(chat_id)
        USER_INFO.pop(chat_id)
        USER_LANGUAGE.pop(chat_id)
        USER_STATUS.pop(chat_id)
        USER_ACTION.pop(chat_id)

        # prepare text and markup
        text: str = prompt.get("success")
        await bot.send_message(chat_id=chat_id, text=text)
        await anon_main(msg=msg)

    else:
        text: str = prompt.get("fail")
        await bot.send_message(chat_id=chat_id, text=text)
        await prompt_password(msg=msg)

    return None


async def debrief_api_delete_doc(cb, response) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_DELETE_DOC.get(USER_LANGUAGE[chat_id])

    # process with api result.
    text: str = prompt.get("success") if response.status_code == 200 else prompt.get("fail")
    await bot.send_message(chat_id=chat_id, text=text)
    await search_docs(cb=cb)

    return None


async def debrief_api_get_chat_infos(msg, response) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id

    # process with api result.
    if response.status_code == 200:

        # update user information
        data = await api_get_user_info(msg=msg)
        USER_LANGUAGE.update({chat_id: data.get("language")})
        await member_main(msg=msg)

    else:
        await anon_main(msg=msg)

    return None


async def debrief_api_get_doc_info(cb, response) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_GET_DOC.get(USER_LANGUAGE.get(chat_id))
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE.get(chat_id))

    # process with api result.
    if response.status_code == 200:
        data: dict = response.json().get("info")
        text: str = prompt.get("success")
        text += f"""
* {prompt.get("site")}:  {data.get('protocol')}://{data.get('site')}
* {prompt.get("username")}:  {data.get('username')}
* {prompt.get("password")}:  {data.get('password')}
* {prompt.get("description")}:  {data.get('description')}
"""
        await bot.send_message(chat_id=chat_id, text=text)

        # new text and markup
        text: str = prompt.get("question")
        markup = quick_markup(values={})
        markup.add(InlineKeyboardButton(text=prompt_button.get("update_doc_btn"), callback_data=f"update_doc_{cb.data}"),
                   InlineKeyboardButton(text=prompt_button.get("delete_doc_btn"), callback_data=f"delete_doc_{cb.data}"))
        markup.add(InlineKeyboardButton(text=prompt_button.get("skip_btn"), callback_data="search_docs"))
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

    else:
        text: str = prompt.get("fail")
        await bot.send_message(chat_id=chat_id, text=text, )
        return None

    return None


async def debrief_api_get_doc_statistics(cb, response) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_DOC_STATISTICS.get(USER_LANGUAGE.get(chat_id))
    prompt_button:dict = PROMPT_BUTTON.get(USER_LANGUAGE.get(chat_id))

    # process with api result.
    if response.status_code == 200:
        data = response.json().get("info")
        text: str = prompt.get("success")
        await bot.send_message(chat_id=chat_id, text=text)

        text = f"""
*  {prompt.get("total")}: {data.get("total")}
*  {prompt.get("length")}: {data.get("length")}
*  {prompt.get("upper")}: {data.get("upper")}
*  {prompt.get("lower")}: {data.get("lower")}
*  {prompt.get("special")}: {data.get("special")}
*  {prompt.get("digit")}: {data.get("digit")}
*  {prompt.get("period")}: {data.get("period")}"""
        await bot.send_message(chat_id=chat_id, text=text)

        text = prompt.get("continue")
        markup = quick_markup(values={})
        markup.add(InlineKeyboardButton(text=prompt_button.get("skip_btn"), callback_data="docs"))
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

    else:
        text: str = prompt.get("fail")
        await bot.send_message(chat_id=chat_id, text=text)
        await docs(cb=cb)

    return None


async def debrief_api_register_license(msg, response) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_REGISTER_LICENSE.get(USER_LANGUAGE.get(chat_id))

    # process with api result
    if response.status_code == 200:
        text: str = prompt.get("success")
        await api_get_user_info(msg=msg)

    else:
        text = prompt.get("fail")
        errors = response.json().get("errors")

        if errors.get("license_info", None) is not None:
            text += prompt.get("invalid")

        elif errors.get("non_field_errors", None):
            text += prompt.get("mismatch_account")

    await bot.send_message(chat_id=chat_id, text=text)
    await settings(msg=msg)
    return None


async def debrief_api_search_docs(msg, response) -> None:
    request_user = msg.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_SEARCH_DOCS.get(USER_LANGUAGE.get(chat_id))
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE.get(chat_id))

    # process with api result.
    if response.status_code == 200:
        data: list = response.json().get("info")

        if len(data) != 0:
            text: str = prompt.get("success").format(len(data))
            markup = quick_markup(values={})

            for info in data:
                markup.add(InlineKeyboardButton(text=info.get("description"), callback_data=info.get("uuid")))

            markup.add(InlineKeyboardButton(text=prompt_button.get("cancel_btn"), callback_data="search_docs"))
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

        else:
            text: str = prompt.get("no_data")
            await bot.send_message(chat_id=chat_id, text=text)
            await search_docs(msg=msg)

    else:
        text: str = prompt.get("fail")
        await bot.send_message(chat_id=chat_id, text=text)
        await search_docs(msg=msg)

    return None


async def debrief_api_signin(response, msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id = request_user.id
    prompt: dict = PROMPT_API_SIGNIN.get(USER_LANGUAGE[chat_id])
    prompt_button: dict = PROMPT_BUTTON.get(USER_LANGUAGE[chat_id])

    # update user information
    USER_ACTION.update({chat_id: "debrief_api_signin"})

    # process with api result.
    if response.status_code == 200:
        text = prompt.get("success")
        await bot.send_message(chat_id=chat_id, text=text)
        await member_main(msg=msg, cb=cb)

    else:
        text = prompt.get("fail")
        await bot.send_message(chat_id=chat_id, text=text)

        text = prompt.get("question_signup")
        markup = quick_markup({})
        markup.add(InlineKeyboardButton(text=prompt_button.get("signup_btn"), callback_data="signup"),
                         InlineKeyboardButton(text=prompt_button.get("signin_btn"), callback_data="signin"))
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

    return None


async def debrief_api_signup(cb, response) -> None:
    chat_id: int = cb.from_user.id
    prompt: dict = PROMPT_API_SIGNUP.get(USER_LANGUAGE[chat_id])

    # process with api result.
    if response.status_code == 200:
        text = prompt.get("success")
        await bot.send_message(chat_id=chat_id, text=text)
        await api_signin(cb=cb)

    else:
        text = prompt.get("fail")
        errors = response.json().get("errors")

        if errors.get("email", None) is not None:
            text += f"\n\n{prompt.get("duplicate_account")}"

        elif errors.get("non_field_errors", None):
            text += f"\n\n{prompt.get("allow_one_account")}"

        await bot.send_message(chat_id=chat_id, text=text)
        await anon_main(cb=cb)

    return None


async def debrief_api_signout(cb, response) -> None:
    request_user = cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_SIGNOUT.get(USER_LANGUAGE[chat_id])

    # process with api result.
    if response.status_code == 200:
        # prepare text and markup
        text = prompt.get("success")

        # update user information
        USER_DATA[chat_id] = {"chat_info": {"msg_name": MESSENGER_CODE, "chat_id": str(chat_id)}}
        USER_STATUS.update({chat_id: "start"})
        USER_ACTION.update({chat_id: "start"})
        USER_INFO.pop(chat_id, None)

    else:
        text = prompt.get("fail")

    await bot.send_message(chat_id=chat_id, text=text)
    await anon_main(cb=cb)
    return None


async def debrief_api_update_account(response, msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_UPDATE_ACCOUNT.get(USER_LANGUAGE[chat_id])

    # process with api result.
    if response.status_code == 200:
        text: str = prompt.get("success")
        data: dict = await api_get_user_info(msg=msg, cb=cb)

        # update edited user info.
        USER_INFO[chat_id] = data if data is not None else USER_INFO[chat_id]

    else:
        text: str = prompt.get("fail")

    await bot.send_message(chat_id=chat_id, text=text)
    await settings(msg=msg, cb=cb)
    return None


async def debrief_api_update_doc(response, msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    prompt: dict = PROMPT_API_UPDATE_DOC.get(USER_LANGUAGE.get(chat_id))

    # process with api result.
    if response.status_code == 200 :
        text: str = prompt.get("success")

    else:
        text: str = prompt.get("fail")
        error: str = response.json().get("errors").get("non_field_errors")[0]

        if error == "license is not valid.":
            text += prompt.get("license_invalid")

        elif error == "license has been expired.":
            text += prompt.get("license_expire")

        elif error == "there is no update on your document.":
            text += prompt.get("no_change")

        elif error == "document is already created.":
            text += prompt.get("duplicate")

    await bot.send_message(chat_id=chat_id, text=text)
    await search_docs(msg=msg, cb=cb)
    return None


async def error_api_connection(msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    language_code = request_user.language_code if request_user.language_code in LANGUAGE_CODE_LIST else DEFAULT_LANGUAGE_CODE
    
    if language_code is None:
        language_code = request_user.language_code if request_user.language_code in LANGUAGE_CODE_LIST else DEFAULT_LANGUAGE_CODE
    
    prompt: dict = PROMPT_CONNECTION_ERROR.get(language_code)

    # prepare text and markup
    text: str = prompt.get("api_conn")
    await bot.send_message(chat_id=chat_id, text=text)
    return None


async def error_db_connection(msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    language_code: str = USER_LANGUAGE.get(chat_id)

    if language_code is None:
        language_code = request_user.language_code if request_user.language_code in LANGUAGE_CODE_LIST else DEFAULT_LANGUAGE_CODE

    prompt: dict = PROMPT_CONNECTION_ERROR.get(language_code)

    # prepare text and markup
    text: str = prompt.get("db_conn")
    await bot.send_message(chat_id=chat_id, text=text)
    return None


@bot.message_handler(func=lambda msg: True)
@bot.callback_query_handler(func=lambda cb: True)
async def invalid_usage(msg=None, cb=None) -> None:
    request_user = msg.from_user if msg is not None else cb.from_user
    chat_id: int = request_user.id
    language_code: str = request_user.language_code
    language_code = language_code if language_code in LANGUAGE_CODE_LIST else DEFAULT_LANGUAGE_CODE
    prompt: dict = PROMPT_INVALID_USAGE.get(language_code)

    text: str = prompt.get("error")
    await bot.send_message(chat_id=chat_id, text=text)
    return None

asyncio.run(bot.polling())
