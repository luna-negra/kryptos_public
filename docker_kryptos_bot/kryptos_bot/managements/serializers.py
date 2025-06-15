# please import handlers classes in core.handlers
# and inherit one of them to your custom handler serializer classes.
from mizuhara.core.handlers.handlers import *
from mizuhara.core.routes import CLIENT_INFO
from managements.apis import *
from datetime import datetime

# please write down your code below.

class DeleteDoc(ReceiverBasic):
    async def send_message(self):
        response = api_delete_doc(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info}, uuid=CLIENT_INFO[self.chat_id].result)
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        await self.bot.send_message(chat_id=self.chat_id, text=translate(domain=domain,
                                                                         key="delete_doc",
                                                                         types=self.types))
        return None


class EditDoc(ReceiverWithInlineMarkup):
    class Meta:
        fields = [
            "edit_doc_with_site",
            "edit_doc_with_username",
            "edit_doc_with_password",
            "edit_doc_with_description",
            "cancel",
        ]
        fields_callback = {
            "cancel": "search_docs",
        }

    def __init__(self, types, **kwargs):
        super(EditDoc, self).__init__(types=types, **kwargs)

    async def pre_process(self) -> bool:
        datetime_now = str(datetime.now()).replace(" ", "T")
        license_info = CLIENT_INFO[self.chat_id].info.get("license_info")

        if license_info.get("kryptos_license_expire") < datetime_now:
            self.bot_markup = None
            self.bot_text = translate(domain="warnings",
                                      key="license_expired",
                                      types=self.types).format(license_info.get("kryptos_license_expire"))
            await self.send_message()
            return False

        elif license_info.get("kryptos_license_issued") > datetime_now:
            self.bot_markup = None
            self.bot_text = translate(domain="warnings",
                                       key="license_inactivated",
                                       types=self.types).format(license_info.get("kryptos_license_issued"))
            await self.send_message()
            return False

        if CLIENT_INFO[self.chat_id].pre_route != "show_doc_info":
            response = api_get_doc_with_uuid(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info},
                                             uuid=CLIENT_INFO[self.chat_id].result)

            data = response.json().get("info")
            site = f"{data.get('protocol')}://{data.get('site')}"
            username = data.get("username")
            password = data.get("password")
            description = data.get("description")
            self.bot_text = translate(domain="handlers",
                                      key="show_doc_info",
                                      types=self.types).format(site, username, password, description)
        return True


class EditDocWithDescription(ReceiverWithForceReply):
    class Meta:
        fields = ["description"]
        fields_text = {
            "description": "description_for_update_doc"
        }

    async def post_process(self):
        self.client_data.update({"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        response = api_update_doc(data=self.client_data, uuid=CLIENT_INFO[self.chat_id].result)
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        self.bot_text = translate(domain=domain,
                                  key="edit_doc_description",
                                  types=self.types)
        return None


class EditDocWithPassword(ReceiverWithForceReply):
    class Meta:
        fields = ["password", "new_password"]
        fields_text = {
            "password": "current_password_for_update_doc",
            "new_password": "new_password_for_update_doc"
        }

    async def post_process(self):
        self.client_data.update({"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        response = api_doc_change_password(data=self.client_data, uuid=CLIENT_INFO[self.chat_id].result)
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        self.bot_text = translate(domain=domain,
                                  key="edit_doc_password",
                                  types=self.types)
        return None


class EditDocWithSite(ReceiverWithForceReply):
    class Meta:
        fields = ["site"]
        fields_text = {
            "site": "site_for_update_doc"
        }
        fields_regex = {
            "site": r"([A-z0-9_\-]+\.){1,3}[A-z0-9_\-]+(:\d{2,5})?$",
        }
        fields_error_msg = {
            "site": "create_doc_regex_site"
        }

    async def post_process(self):
        site = self.client_data.get("site")
        protocol = "https"

        if len(site.split("://")) == 2:
            tmp = site.split("://")
            site = tmp[1]
            protocol = tmp[0]

        self.client_data.update({
            "chat_info": CLIENT_INFO[self.chat_id].chat_info,
            "site": site,
            "protocol": protocol,
        })

        response = api_update_doc(data=self.client_data, uuid=CLIENT_INFO[self.chat_id].result)
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        self.bot_text = translate(domain=domain,
                                  key="edit_doc_site",
                                  types=self.types)
        return None


class EditDocUsername(ReceiverWithForceReply):
    class Meta:
        fields = ["username"]
        fields_text = {
            "username": "username_for_update_doc"
        }

    async def post_process(self):
        self.client_data.update({"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        response = api_update_doc(data=self.client_data, uuid=CLIENT_INFO[self.chat_id].result)
        domain: str = "handlers" if response.status_code == 200 else "warnings"
        self.bot_text = translate(domain=domain,
                                  key="edit_doc_username",
                                  types=self.types)


class Management(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["register_new_doc", "search_docs", "statistics", "cancel"]
        fields_callback = {"cancel": "main"}

    def __init__(self, types, **kwargs):
        super(Management, self).__init__(types=types, **kwargs)
        self.bot_text = translate(domain="handlers", key="management", types=self.types)


class RegisterNewDoc(ReceiverWithForceReply):
    class Meta:
        fields = ["site", "username", "password", "description",]
        fields_text = {
            "site": "site_for_new_doc",
            "username": "username_for_new_doc",
            "password": "password_for_new_doc",
            "description": "description_for_new_doc",
        }
        fields_regex = {
            "site": r"([A-z0-9_\-]+\.){1,3}[A-z0-9_\-]+(:\d{2,5})?$",
        }
        fields_error_msg = {
            "site": "create_doc_regex_site"
        }

    async def pre_process(self) -> bool:
        datetime_now = str(datetime.now()).replace(" ", "T")
        license_info = CLIENT_INFO[self.chat_id].info.get("license_info")

        if license_info.get("kryptos_license_expired", None) is not None:
            if license_info.get("kryptos_license_expire") < datetime_now:
                self.bot_markup = None
                self.bot_text = translate(domain="warnings",
                                          key="license_expired",
                                          types=self.types).format(license_info.get("kryptos_license_expire"))
                return False

            elif license_info.get("kryptos_license_issued") > datetime_now:
                self.bot_markup = None
                self.bot_text = translate(domain="warnings",
                                          key="license_inactivated",
                                          types=self.types).format(license_info.get("kryptos_license_issued"))
                return False

        response = api_search_docs(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        doc_number: int = len(response.json().get("info"))
        license_amount: int = int(license_info.get("kryptos_license").get("documents")) if license_info.get("kryptos_license") else 5
        if doc_number >= license_amount:
            self.bot_markup = None
            self.bot_text = translate(domain="warnings",
                                      key="license_limit",
                                      types=self.types).format(license_amount)
            return False

        return True


    async def post_process(self):
        site: str = self.client_data.get("site").lower()
        protocol: str = "https"

        if len(site.split("://")) == 2:
            tmp = site.split("://")
            protocol, site = tmp[0], tmp[1]

        self.client_data.update({
            "site": site,
            "protocol": protocol,
            "chat_info": CLIENT_INFO[self.chat_id].chat_info,
        })
        response = api_register_new_doc(data=self.client_data)

        if response.status_code == 200:
            self.bot_text = translate(domain="handlers", key="register_new_doc", types=self.types)

        else:
            err_msg: str = response.json().get("errors").get("non_field_errors")[0]

            if err_msg.startswith("you reached license limit."):
                key = "create_doc_license_limit"

            elif err_msg.startswith("license is not valid."):
                key = "create_doc_invalid_license"

            elif err_msg.startswith("license has been expired."):
                key = "create_doc_expired_license"

            elif err_msg.startswith("document is already created."):
                key = "create_doc_already_exist"

            else:
                key = "create_doc_without_unknown_reason"

            self.bot_text = translate(domain="warnings", key=key, types=self.types)

        return None


class SearchDocs(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["search_all_docs", "search_docs_with_url", "search_docs_with_description", "cancel"]
        fields_callback = {"cancel": "management"}

    def __init__(self, types, **kwargs):
        super(SearchDocs, self).__init__(types=types, **kwargs)
        self.bot_text = translate(domain="handlers", key="search_account", types=self.types)


class SearchAllDocs(ReceiverBasic):
    async def send_message(self):
        response = api_search_docs(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        CLIENT_INFO[self.chat_id].update(result=response.json().get("info") if response.status_code == 200 else None)
        return response.status_code == 200


class SearchDocsWithURL(ReceiverWithForceReply):
    class Meta:
        fields = ["site"]
        fields_text = {"site": "site_for_search_docs"}
        fields_regex = {
            "site": r"([A-z0-9_\-]+\.){1,3}[A-z0-9_\-]+(:\d{4,5})?$"
        }

    async def post_process(self):
        tmp = self.client_data.pop("site").split("://")
        protocol, site = (None, tmp[0]) if len(tmp) == 1 else (tmp[0], tmp[1])
        search_params = {"site": site, "protocol": protocol} if protocol is not None else {"site": site}

        self.client_data.update({
            "chat_info": CLIENT_INFO[self.chat_id].chat_info,
            "search_q": search_params
        })

        response = api_search_docs(data=self.client_data)
        CLIENT_INFO[self.chat_id].update(result=response.json().get("info") if response.status_code == 200 else None)
        return None


class SearchAccountsWithDescription(ReceiverWithForceReply):
    class Meta:
        fields = ["description"]
        fields_text = {"description": "description_for_search_docs"} #

    async def post_process(self):
        description = self.client_data.pop("description")
        self.client_data.update({
            "chat_info": CLIENT_INFO[self.chat_id].chat_info,
            "search_q": {"description": description},
        })

        response = api_search_docs(data=self.client_data)
        CLIENT_INFO[self.chat_id].update(result=response.json().get("info") if response.status_code == 200 else None)
        return None


class SearchResult(ReceiverWithInlineMarkupPagination):
    class Meta:
        fields = ["empty"]

    def __init__(self, types, **kwargs):
        self.Meta.fields = []
        self.Meta.fields_callback = {}
        result = CLIENT_INFO[types.from_user.id].result

        if len(result):
            self.flag = True
            for doc in result:
                self.Meta.fields.append(doc.get("description"))
                self.Meta.fields_callback.update({doc.get("description"): doc.get("uuid")})

        else:
            self.flag = False

        super(SearchResult, self).__init__(types=types, **kwargs)

    async def send_message(self):
        domain: str = "handlers" if self.flag else "warnings"
        self.bot_text = translate(domain=domain, key="search_result_list_text", types=self.types).format(len(self.Meta.fields))
        await super().send_message() if self.flag else await self.bot.send_message(chat_id=self.chat_id,
                                                                                   text=self.bot_text)
        return self.flag


class ShowDocInfo(ReceiverWithInlineMarkup):
    class Meta:
        fields = ["edit_doc", "delete_doc", "continue"]
        fields_callback = {
            "continue": "search_docs",
        }

    def __init__(self, types, **kwargs):
        super(ShowDocInfo, self).__init__(types=types, **kwargs)

        data = getattr(types, "data")
        uuid = data if data != "edit_doc" else CLIENT_INFO[self.chat_id].result
        self.get_info_with_uuid(uuid=uuid)

    def get_info_with_uuid(self, uuid):
        response = api_get_doc_with_uuid(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info}, uuid=uuid)
        if response.status_code == 200:
            info: dict = response.json().get("info")
            site: str = f"{info.get('protocol')}://{info.get('site')}"
            username: str = info.get("username")
            password: str = info.get("password")
            description: str = info.get("description")

            self.bot_text = translate(domain="handlers",
                                      key="show_doc_info",
                                      types=self.types).format(site, username, password, description)
            CLIENT_INFO[self.chat_id].update(result=uuid)

        else:
            self.bot_text = translate(domain="warnings", key="show_doc_info", types=self.types)

        return None


class Statistics(ResultShowingWithInlineMarkup):
    class Meta:
        fields = ["continue"]
        fields_callback: dict = {
            "continue": None
        }

    def __init__(self, types, link_route: str, **kwargs):
        super(Statistics, self).__init__(types=types, link_route=link_route, **kwargs)

    async def pre_process(self):
        response = api_get_statistics(data={"chat_info": CLIENT_INFO[self.chat_id].chat_info})
        if response.status_code == 200:
            data = response.json().get("info")
            total = data.get("total")
            v_length = data.get("length")
            v_upper = data.get("upper")
            v_lower = data.get("lower")
            v_special = data.get("special")
            v_digit = data.get("digit")
            v_period = data.get("period")

            self.bot_text = translate(domain="handlers",
                                      key="statistics",
                                      types=self.types).format(total, v_length, v_upper, v_lower, v_special, v_digit, v_period)

        else:
            self.bot_text = translate(domain="warnings", key="statistics", types=self.types)

        return None