# please import handlers classes in core.handlers
# and inherit one of them to your custom handler serializer classes.
import io, yaml
from os import getenv
from pyzipper import (is_zipfile, AESZipFile,)
from mizuhara.core.handlers.handlers import *
from mizuhara.core.handlers.file.docs import ReceiverWithZipFile
from mizuhara.core.routes import CLIENT_INFO

from members.apis import api_get_user_info
from settings.apis import *


# please write down your code below.

class ChangeFirstName(ReceiverWithForceReply):
    class Meta:
        fields = ["first_name"]
        fields_text = {"first_name": "edit_first_name"}

    async def post_process(self):
        self.client_data.update({"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        response = api_update_user_info(data=self.client_data)
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        self.bot_text = translate(domain=domain, key="update_first_name", types=self.types)
        return None


class ChangeLanguage(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["en", "ja", "ko", "cancel"]
        fields_callback = {
            "cancel": "show_settings"
        }

    def __init__(self, types, **kwargs):
        super(ChangeLanguage, self).__init__(types=types, **kwargs)
        self.bot_text = translate(domain="handlers",
                                  key="change_language",
                                  types=self.types)

    async def send_message(self):
        if self.types.data == "change_language":
            await super().send_message()
            return None

        domain: str = "handlers" if await self.post_process() else "warnings"
        await self.bot.send_message(chat_id=self.chat_id,
                                    text=translate(domain=domain, key="update_language", types=self.types))
        return True

    async def post_process(self):
        data = {"language": self.client_response, "chat_info": CLIENT_INFO[self.chat_id].chat_info}
        response = api_update_user_info(data=data)
        result = response.status_code == 200

        if result:
            CLIENT_INFO[self.chat_id].update(language=self.client_response)

        return result


class ChangeLastName(ReceiverWithForceReply):
    class Meta:
        fields = ["last_name"]
        fields_text = {"last_name": "edit_last_name"}

    async def post_process(self):
        self.client_data.update({"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        response = api_update_user_info(data=self.client_data)
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        self.bot_text = translate(domain=domain, key="update_last_name", types=self.types)
        return None


class ChangeMaxAccessLimit(ReceiverWithForceReply):
    class Meta:
        fields = ["max_access_try"]
        fields_regex = {
            "max_access_try": ["^[3-5]$"]
        }
        fields_error_msg = {
            "max_access_try": "warn_out_of_range_max_access"
        }

    async def post_process(self):
        self.client_data.update({"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        response = api_update_user_info(data=self.client_data)
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        self.bot_text = translate(domain=domain, key="update_max_access_try", types=self.types)
        return None


class ChangeName(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["change_first_name", "change_last_name", "cancel"]
        fields_callback = {
            "cancel": "show_settings"
        }

    def __init__(self, types, **kwargs):
        super(ChangeName, self).__init__(types=types, **kwargs)
        self.bot_text = translate(domain="handlers", key="change_name", types=self.types)


class ChangePassword(ReceiverWithForceReply):
    class Meta:
        fields = ["password", "new_password"]
        fields_text = {
            "password": "password_for_change_password",
            "new_password": "new_password_for_change_password"
        }
        fields_regex = {
            "new_password": (
                "[A-Z]+",
                "[a-z]+",
                "[0-9]+",
                "[!@#$%^&*()_+\\-=]+",
            )}
        fields_error_msg = {
            "new_password": (
                "warn_password_no_upper",
                "warn_password_no_lower",
                "warn_password_no_digit",
                "warn_password_no_special",
            )
        }

    async def post_process(self):
        self.client_data.update({"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        key: str = "update_password"
        response = api_update_password(data=self.client_data)
        if response.status_code == 200:
            domain: str = "handlers"
            CLIENT_INFO[self.chat_id].result = True

        else:
            domain: str = "warnings"
            errors = response.json().get("errors").get("non_field_errors")[0]
            if errors == "current password is not match.":
               key = "update_password_mismatch_current_password"
            CLIENT_INFO[self.chat_id].result = None

        self.bot_text = translate(domain=domain, key=key, types=self.types)
        return None


class ChangeVisibility(ReceiverWithForceReply):
    class Meta:
        fields = ["visibility"]
        fields_regex = {
            "visibility": "^(?:[2-7][0-9]|80)$"
        }
        fields_error_msg = {
            "visibility": "warn_out_of_range_visibility"
        }

    async def post_process(self):
        self.client_data.update({"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        response = api_update_user_info(data=self.client_data)
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        self.bot_text = translate(domain=domain, key="update_visibility", types=self.types)
        return None


class DeleteKryptos(ReceiverWithForceReply):
    class Meta:
        fields = ["password"]
        fields_text = {"password": "delete_kryptos_password"}

    async def post_process(self):
        self.client_data.update({"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        response = api_delete_kryptos_account(data=self.client_data)
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        self.bot_text = translate(domain=domain, key="delete_kryptos", types=self.types)
        CLIENT_INFO[self.chat_id].result = response.status_code == 200
        return None


class LicenseSettings(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["register_license", "continue"]
        fields_callback = {
            "continue": "settings"
        }

    def __init__(self, types, **kwargs):
        super(LicenseSettings, self).__init__(types=types, **kwargs)
        license_info = CLIENT_INFO[self.chat_id].info.get("license_info")
        if license_info != {}:
            license_version: str = license_info.get("kryptos_version")
            total_number: int = license_info.get("kryptos_license").get("documents")
            expiration_date: str = str(license_info.get("kryptos_license_issued")).replace("T", " ")
            issue_date: str = str(license_info.get("kryptos_license_expire")).replace("T", " ")

        else:
            license_version: str = "Default License"
            total_number: int = 5
            expiration_date: str = "Unlimited"
            issue_date: str = "Not Assigned"

        self.bot_text = translate(domain="handlers",
                                  key="show_current_license_info",
                                  types=self.types).format(license_version, total_number, expiration_date, issue_date)


class RegisterLicense(ReceiverWithZipFile):
    def __init__(self, types, link_route, **kwargs):
        super(RegisterLicense, self).__init__(types=types, link_route=link_route, **kwargs)
        self.bot_text = translate(domain="handlers", key="upload_license_file", types=self.types)

    async def post_process(self):
        flag = False
        zip_file = io.BytesIO(self.file)

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
            data = {
                "chat_info": CLIENT_INFO[self.chat_id].chat_info,
                "license_info": contents
            }

            response = api_register_license(data=data)

            if response.status_code == 200:
                domain: str = "handlers"
                key: str = "register_license"

            else:
                domain: str = "warnings"
                try:
                    errors = response.json().get("errors").get("non_field_errors")[0]

                except TypeError:
                    errors = response.json().get("errors").get("license_info")[0]

                if errors == "License has been expired.":
                    key = "register_license_expire"

                elif errors == "License is not in activation status.":
                    key = "register_license_not_activated"

                elif errors == "License is not valid for current account.":
                    key = "register_license_invalid_user"

                else:
                    key = "register_license"

            self.bot_text = translate(domain=domain, key=key, types=self.types)
            response = api_get_user_info(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info})
            CLIENT_INFO[self.chat_id].update(info=response.json().get("info"))

        else:
            domain: str = "warnings"
            self.bot_text = translate(domain=domain, key="register_license_invalid", types=self.types)

        await self.bot.send_message(chat_id=self.chat_id, text=self.bot_text)
        return None


class Settings(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["show_settings", "license_settings", "delete_kryptos", "cancel"]
        fields_callback = {"cancel": "main"}

    def __init__(self, types, **kwargs):
        super(Settings, self).__init__(types=types, **kwargs)
        self.bot_text = translate(domain="handlers",
                                  key="settings_prompt",
                                  types=self.types)


class ShowCurrentSettings(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["change_name", "change_language", "change_max_access_limit", "change_visibility",  "change_password", "continue"]
        fields_callback = {"continue": "settings"}

    def __init__(self, types, **kwargs):
        super(ShowCurrentSettings, self).__init__(types=types, **kwargs)
        response = api_get_user_info(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info})

        if response.status_code == 200:
            CLIENT_INFO[self.chat_id].update(info=response.json().get("info"))

        data = CLIENT_INFO[self.chat_id].info
        email: str = data.get("email")
        first_name: str = data.get("first_name")
        last_name: str = data.get("last_name")
        language: str = translate(domain="buttons", key=data.get("language"), types=self.types)
        max_access_try: int = data.get("max_access_try")
        visibility: int = data.get("visibility")
        last_signin: str = data.get("last_access_datetime").replace("T", " ").split(".")[0]
        last_signout: str = data.get("last_signout_datetime").replace("T", " ").split(".")[0]
        last_update: str = data.get("last_updated_datetime").replace("T", " ").split(".")[0]
        registered: str = data.get("registered_datetime").replace("T", " ").split(".")[0]
        self.bot_text = translate(domain="handlers",
                                  key="show_current_kryptos_settings",
                                  types=self.types).format(email, first_name, last_name, language, max_access_try,
                                                           visibility, last_signin, last_signout, last_update, registered)
        CLIENT_INFO[self.chat_id].result = self.bot_text
