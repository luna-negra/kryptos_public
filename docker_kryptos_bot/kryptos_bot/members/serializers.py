# please import handlers classes in core.handlers
# and inherit one of them to your custom handler serializer classes.
from mizuhara.core.handlers.accounts import *
from mizuhara.core.handlers.handlers import *
from mizuhara.core.routes import CLIENT_INFO


# please write down your code below.
from mizuhara.translation import translate
from members.apis import *


class ActivateAccount(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["input_code", "send_code"]

    async def send_message(self) -> None:
        self.bot_text = translate(domain="handlers", key="explain_activation_code", types=self.types).format(
            translate(domain="buttons", key="send_code", types=self.types),
            translate(domain="buttons", key="input_code", types=self.types)
        )
        await super().send_message()

        api_send_code(data={
            "chat_info": CLIENT_INFO[self.chat_id].__dict__.get("chat_info"),
            "mail_type": "activation"
        })
        return None

    async def check_activation(self) -> bool:
        response = api_get_user_activation_info(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info})

        if response.status_code == 200 and response.json().get("info") :
            response = api_get_user_info(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info})

            if response.status_code == 200:
                data = response.json()
                CLIENT_INFO[self.chat_id].update(
                    info=data.get("info"),
                    language=data.get("info").get("language")
                )
            return True

        return False


class InputActivation(ReceiverWithForceReply):
    class Meta:
        fields = ["activation_code"]

    def __init__(self, types, link_route, **kwargs):
        super().__init__(types=types, link_route=link_route, **kwargs)
        self.bot_text = translate(domain="handlers",
                                  key="activation_code",
                                  types=self.types)

    async def send_code(self) -> None:
        response = api_send_code(data={
            "chat_info": CLIENT_INFO[self.chat_id].__dict__.get("chat_info"),
            "mail_type": "activation"
        })
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        await self.bot.send_message(chat_id=self.chat_id, text=translate(domain=domain, key="send_code", types=self.types))
        return None

    async def post_process(self):
        self.client_data.update({"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        response = api_activate_account(data=self.client_data)
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        self.bot_text = translate(domain=domain, key="activation", types=self.types)
        return None


class Main(ReceiverBasic):
    async def send_message(self) -> bool:
        response = api_check_chat(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        CLIENT_INFO[self.chat_id].is_signin = response.json().get("result", False)
        return CLIENT_INFO[self.chat_id].is_signin


class MainAnon(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["signin", "signup"]

    def __init__(self, types, **kwargs):
        super(MainAnon, self).__init__(types=types, **kwargs)
        self.bot_text = translate(domain="handlers", key="welcome_anon", types=self.types)


class MainMember(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["management", "settings", "signout"]

    def __init__(self, types, **kwargs):
        super(MainMember, self).__init__(types, **kwargs)
        self.bot_text = translate(domain="handlers",
                                  key="welcome_member",
                                  types=self.types).format(CLIENT_INFO[self.chat_id].info.get("first_name"))


class SignIn(SignInBasic):
    async def post_process(self):
        CLIENT_INFO[self.chat_id].chat_info.update({"is_signed_in": False})
        self.client_data.update({"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        response = api_signin(data=self.client_data)

        domain: str = "handlers" if response.status_code == 200 and response.json().get("result") else "warnings"
        CLIENT_INFO[self.chat_id].chat_info.update({"is_signed_in": True})
        self.bot_text = translate(domain=domain, key="signin", types=self.types)
        return None


class SignOut(SignOutBasic):
    async def post_process(self):
        response = api_signout(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        if response.status_code == 200:
            CLIENT_INFO.pop(self.chat_id)
            domain: str = "handlers"

        else:
            domain: str = "warnings"

        self.bot_text = translate(domain=domain, key="signout", types=self.types)
        return None


class SignUp(SignUpBasic):
    async def post_process(self):
        key = "signup"

        self.client_data.update({
            "chat_info": CLIENT_INFO[self.chat_id].chat_info,
            "first_name": self.request_user.first_name,
            "last_name": self.request_user.last_name,
            "language": CLIENT_INFO[self.chat_id].language,
        })
        response = api_signup(data=self.client_data)

        if response.status_code == 200:
            CLIENT_INFO[self.chat_id].is_signed_in = True
            domain: str = "handlers"

        else:
            domain: str = "warnings"
            key = "sign_up_duplicate"

        self.bot_text = translate(domain=domain, key=key, types=self.types)
        return None
