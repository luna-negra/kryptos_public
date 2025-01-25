from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework.exceptions import ValidationError

from accounts.models import (Accounts,
                             ChatInfos,
                             Tokens,
                             datetime)
from documents.models import Documents
from tools.regex import (regex_match,
                         REGEX_PASSWORD_DIGIT,
                         REGEX_UUID,)


USER_MODEL = Accounts
DOCUMENTS_MODEL = Documents


class ChatAccessSerializer(DocumentSerializer):
    """
    access check class via sns chatbot.
    do not use it directly.

    """

    class Meta:
        model = None
        fields = ()

    def __init__(self, *args, **kwargs):
        self._chat_info = kwargs.pop("chat_info", None)
        self._auth_str = kwargs.pop("auth_str", None)
        super(ChatAccessSerializer, self).__init__(*args, **kwargs)

    def validate(self, data: dict) -> dict:
        if self._chat_info is not None:
            messenger: str | None = self._chat_info.get("msg_name", None)
            chat_id: str | None = self._chat_info.get("chat_id", None)
            is_signed_in: bool = self._chat_info.get("is_signed_in", None)

            # Validate Telegram Info
            condition1: bool = messenger == "TLGR" and len(chat_id) == 10
            condition2: bool = regex_match(pattern=REGEX_PASSWORD_DIGIT, string=chat_id) is not None
            condition3: bool = isinstance(is_signed_in, bool)

            if not condition1 or not condition2 or not condition3:
                raise ValidationError("Bad Request.")

        return data


class AuthAccessSerializer(ChatAccessSerializer):
    """
    authentication class without activation status.
    do not use it directly.

    """

    def __init__(self, *args, **kwargs):
        self._account = None
        super(AuthAccessSerializer, self).__init__(*args, **kwargs)

    def validate(self, data) -> dict:
        stored_info = None

        if self._chat_info is None and self._auth_str is None:
            raise ValidationError("you have to sign in first.")

        if self._chat_info is not None:
            super(AuthAccessSerializer, self).validate(data=data)
            stored_info = ChatInfos.objects(**self._chat_info).first()
            if stored_info is None:
                raise ValidationError("you have to sign in first.")

        if self._account is None and self._auth_str is not None:
            stored_info = Tokens.objects(token=self._auth_str).first()

            if stored_info is None or not stored_info.is_valid():
                raise ValidationError("access session is expired. please sign in again.")

        self._account = stored_info.get_account() if stored_info is not None else None

        if self._account is None:
            raise ValidationError("account is not exist.")

        return data

    def save(self):
        pass


class ActiveAccessSerializer(AuthAccessSerializer):
    """
    authentication class with activation status.
    do not use it directly.

    """

    def validate(self, data:dict) -> dict:
        super(ActiveAccessSerializer, self).validate(data=data)

        if not self._account.is_active:
            raise ValidationError("account is not activated yet")

        return data


class SuperuserAccessSerializer(ActiveAccessSerializer):
    """
    superuser authentication class
    do not use it directly.

    """

    def validate(self, data:dict) -> dict:
        super(ActiveAccessSerializer, self).validate(data=data)

        if not self._account.is_superuser:
            raise ValidationError("do not have any privilege.")

        return data


class AccountChatAccessSerializer(ChatAccessSerializer):
    """
    access check class for accounts application.
    do not use it directly.

    """
    class Meta:
        model = Accounts
        fields = ()


class AccountAuthAccessSerializer(AuthAccessSerializer):
    """
    authentication class without activation status for accounts application.
    do not use it directly.

    """

    class Meta:
        model = Accounts
        fields = ()


class AccountActiveAccessSerializer(ActiveAccessSerializer):
    """
    authentication class with activation status for accounts application.
    do not use it directly.

    """

    class Meta:
        model = Accounts
        fields = ()


class DocumentAuthAccessSerializer(AuthAccessSerializer):
    """
    authentication class without activation status for documents application.
    do not use it directly.

    """

    class Meta:
        model = Documents
        fields = ()