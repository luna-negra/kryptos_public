from uuid import uuid4
import mongoengine as mg
from django.contrib.auth.hashers import (make_password,
                                         check_password,)

from documents.models import Documents
from tools.clk import Codebook, CLK
from tools import apply_asterisk
from tools.datetime import (EPOCH_DATETIME,
                            EPOCH_FORMAT,
                            datetime,
                            timedelta,)


MAX_ACCESS_TRY: int = 5
MESSENGER_CHOICE: dict = {
    "TLGR": "Telegram",
}
LANGUAGE_CHOICE: dict = {
    "en": "English",
    "jp": "日本語",
    "ko": "한국어"
}


class Codes(mg.Document):
    uuid = mg.UUIDField(primary_key=True, required=True, binary=False)
    codebook = mg.StringField(required=True, min_length=63, max_length=63)
    last_updated_datetime = mg.DateTimeField(required=True, default=EPOCH_DATETIME)
    registered_datetime = mg.DateTimeField(required=True, default=EPOCH_DATETIME)


    def __str__(self) -> str:
        return str(self.uuid)


    def modify(self, *args, **kwargs) -> None:
        kwargs.update({
            "codebook": Codebook.generate(),
            "last_updated_datetime": datetime.now()
        })
        super(Codes, self).modify(*args, **kwargs)
        return None


    def save(self, *args, **kwargs) -> None:
        if self.registered_datetime == EPOCH_DATETIME:
            self.registered_datetime = datetime.now()
        super(Codes, self).save(*args, **kwargs)
        return None


class Tokens(mg.Document):
    uuid = mg.UUIDField(primary_key=True, required=True, binary=False)
    token = mg.StringField(required=True, min_length=277, max_length=277, default="A" * 277)
    issued_datetime = mg.DateTimeField(required=True, default=EPOCH_DATETIME)
    expire_datetime = mg.DateTimeField(required=True, default=EPOCH_DATETIME)


    def __str__(self) -> str:
        return str(self.uuid)


    def get_account(self):
        return Accounts.objects(pk=self.uuid).first()


    def get_res_data(self) -> dict:
        res_data = self.to_mongo().to_dict()
        res_data["is_active"] = self.get_account().is_active
        res_data.pop("_id")
        return res_data


    def logout(self) -> None:
        self.expire_datetime = datetime.now()
        self.save()
        return None


    def is_valid(self) -> bool:
        if datetime.now() < self.expire_datetime:
            return True

        return False


class ChatInfos(mg.Document):
    uuid = mg.UUIDField(primary_key=True, required=True, binary=False)
    msg_name = mg.StringField(required=True, choice=MESSENGER_CHOICE)
    chat_id = mg.StringField(required=True)
    is_signed_in = mg.BooleanField(required=True, default=False)
    last_updated_datetime = mg.DateTimeField(default=EPOCH_DATETIME)
    registered_datetime = mg.DateTimeField(default=EPOCH_DATETIME)


    def __str__(self) -> str:
        return str(self.uuid)


    def modify(self, *args, **kwargs) -> None:
        kwargs.update({"last_updated_datetime": datetime.now()})
        super(ChatInfos, self).modify(*args, **kwargs)
        return None


    def get_account(self):
        return Accounts.objects(pk=self.uuid).first()


    def save(self, **kwargs):
        if self.registered_datetime == EPOCH_DATETIME:
            self.registered_datetime = datetime.now()
        super(ChatInfos, self).save(**kwargs)



class Accounts(mg.Document):
    uuid = mg.UUIDField(primary_key=True, required=True, binary=False, default=uuid4)

    # user realm
    email = mg.EmailField(required=True)
    password = mg.StringField(required=True, min_length=8, max_length=256)
    first_name = mg.StringField(required=True, min_length=1, max_length=20, regex=r"^\w+$")
    last_name = mg.StringField(required=True, min_length=1, max_length=20, regex=r"^\w+$")
    language = mg.StringField(required=True, min_length=2, max_length=2, regex=r"^[a-z]{2}$", default="en")
    max_access_try = mg.IntField(required=True, min_value=3, max_value=5, default=MAX_ACCESS_TRY)
    visibility = mg.IntField(required=True, min_value=20, max_value=80, default=30)

    # admin realm
    consecutive_access_fail = mg.IntField(required=True, default=0)
    is_active = mg.BooleanField(required=True, default=False)
    is_superuser = mg.BooleanField(required=True, default=False)
    groups = mg.ListField(required=False)
    license_info = mg.DictField(required=False)

    # django realm
    last_access_datetime = mg.DateTimeField(required=True, default=EPOCH_DATETIME)
    last_signout_datetime = mg.DateTimeField(required=True, default=EPOCH_DATETIME)
    last_updated_datetime = mg.DateTimeField(required=True, default=EPOCH_DATETIME)
    registered_datetime = mg.DateTimeField(required=True, default=EPOCH_DATETIME)


    def __str__(self) -> str:
        return str(self.uuid)


    def _asterisk_doc(self, document:Documents) -> dict:
        visibility: float = float(self.visibility / 100)
        data: dict = document.get_res_data()
        enc_password: str = data.get("password")
        text_password: str = CLK(codebook=self.get_code(), string=enc_password).get_result()

        data.update({"password": apply_asterisk(string=text_password, visibility=visibility)})
        return data


    def check_password(self, password:str) -> bool:
        return check_password(password=password, encoded=self.password)


    def check_activation_code(self, activation_code:str) -> bool:
        if self.__get_code().codebook.startswith(activation_code):
            return True

        return False


    def change_code(self) -> None:
        code = self.__get_code()
        documents_list = self.__get_documents_list()
        prev_code = code.codebook

        code.modify()
        new_code = code.codebook

        for doc in documents_list:
            plain_pw: str = CLK(codebook=prev_code, string=doc.password).get_result()
            doc.password = CLK(codebook=new_code, string=plain_pw).get_result()
            doc.save()

        return None


    def delete(self, *args, **kwargs) -> None:
        code = self.__get_code()
        token = self.get_token()
        chat_id = self.get_chat_info()
        documents = self.__get_documents_list()

        if code is not None:
            code.delete()

        if token is not None:
            token.delete()

        if chat_id is not None:
            chat_id.delete()

        for doc in documents:
            doc.delete()

        super(Accounts, self).delete(*args, **kwargs)
        return None


    def get_activation_code(self) -> str:
        return self.__get_code().codebook[:6]


    def get_chat_info(self) -> ChatInfos:
        return ChatInfos.objects(pk=self.uuid).first()


    def get_code(self) -> str:
        return self.__get_code().codebook


    def __get_code(self) -> Codes:
        return Codes.objects(pk=self.uuid).first()


    def get_documents_statistics(self) -> dict:
        all_docs_list: list = self.__get_documents_list()
        data: dict = {
            "total": len(all_docs_list),
            "length": 0,
            "upper": 0,
            "lower": 0,
            "special": 0,
            "digit": 0,
            "period": 0,
        }

        for doc in all_docs_list:
            data["length"] += 1 if doc.is_length_violate else 0
            data["upper"] += 1 if doc.is_upper_violate else 0
            data["lower"] += 1 if doc.is_lower_violate else 0
            data["special"] += 1 if doc.is_special_violate else 0
            data["digit"] += 1 if doc.is_digit_violate else 0

            if doc.last_updated_datetime.year != 1970:
                data["period"] += 1 if datetime.now() - doc.last_updated_datetime > timedelta(days=90)  else 0

            else:
                data["period"] += 1 if datetime.now() - doc.registered_datetime > timedelta(days=90)  else 0

        return data


    def get_information(self, exclude=("_id",
                                       "password",
                                       "consecutive_access_fail",
                                       "is_superuser")) -> dict:
        data = self.to_mongo().to_dict()

        if data.get("license_info").get("kryptos_digital_sign", None) is not None:
            data.get("license_info").pop("kryptos_digital_sign")

        for field in exclude:
            data.pop(field)

        return data


    def get_license_information(self) -> dict:
        return self.license_info


    def get_token(self) -> Tokens:
        return Tokens.objects(pk=self.uuid).first()


    def __get_documents_list(self) -> list:
        return Documents.objects(account=self.uuid)


    def __make_password(self) -> None:
        if not self.password.startswith("pbkdf2_sha256$") and not len(self.password) == 256:
            self.password = make_password(password=self.password)

        return None


    def modify(self, signin=False, *args, **kwargs) -> None:
        if not signin:
            kwargs.update({"last_updated_datetime": datetime.now()})

        if kwargs.get("license_info", None) is not None:
            issue_datetime: str = kwargs["license_info"].get("kryptos_license_issued")
            expire_datetime: str = kwargs["license_info"].get("kryptos_license_expire")
            kwargs["license_info"].update({"kryptos_license_issued": datetime.strptime(issue_datetime, EPOCH_FORMAT),
                                           "kryptos_license_expire": datetime.strptime(expire_datetime, EPOCH_FORMAT)})

        super(Accounts, self).modify(*args, **kwargs)

        # if you change password, you need to execute save() method.
        return None


    def modify_code(self) -> None:
        code = self.__get_code()
        documents = self.__get_documents_list()
        pre_code = code.codebook

        code.modify()

        for doc in documents:
            plain_pw = CLK(codebook=pre_code, string=doc.password).get_result()
            doc.modify({"password": plain_pw})

        return None


    def save(self, *args, **kwargs) -> None:
        code = self.__get_code()
        token = self.get_token()
        chat_id: dict = kwargs

        if chat_id != {} and self.get_chat_info() is None:
            ChatInfos(uuid=self.uuid, **chat_id).save()
            self.update(**{"last_access_datetime": datetime.now()})

        if code is None:
            code = Codes(uuid=self.uuid, codebook=Codebook.generate())
            code.modify()
            code.save()

        if token is None:
            Tokens(uuid=self.uuid).save()

        if self.registered_datetime == EPOCH_DATETIME:
            self.registered_datetime = datetime.now()

        self.__make_password()
        super(Accounts, self).save(*args, **kwargs)
        return None


    def signout(self, token=None, chat_info=None) -> None:
        if token is not None:
            token.modify(**{"expire_datetime":datetime.now()})

        elif chat_info is not None:
            chat_info.modify(**{"is_signed_in": False})

        self.modify(signin=True, **{"last_signout_datetime": datetime.now()})
        return None
