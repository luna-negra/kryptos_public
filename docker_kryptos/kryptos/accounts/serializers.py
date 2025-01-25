from django.conf import settings
from django.utils.text import capfirst
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail

from .backends import CustomUserBackend
from core.serializers import (AccountChatAccessSerializer,
                              AccountAuthAccessSerializer,
                              AccountActiveAccessSerializer,
                              ValidationError,
                              Accounts,
                              ChatInfos)


### ChatAccess
class CheckChatInfoSerializer(AccountChatAccessSerializer):
    def validate(self, data:dict) -> dict:

        if self._chat_info is None:
            raise ValidationError("Bad Request")

        super(CheckChatInfoSerializer, self).validate(data=data)

        if ChatInfos.objects(**self._chat_info).first() is None:
            raise ValidationError("Unable to find account.")

        return data

    def save(self) -> None:
        return None


class AccountSignInSerializer(AccountChatAccessSerializer):
    class Meta:
        model = AccountChatAccessSerializer.Meta.model
        fields = AccountChatAccessSerializer.Meta.fields + ("email", "password",)

    def __init__(self, *args, **kwargs):
        self._account = None
        super(AccountSignInSerializer, self).__init__(*args, **kwargs)

    def validate(self, data: dict) -> dict:
        super(AccountSignInSerializer, self).validate(data=data)

        email: str | None = data.get("email", None)
        password: str | None = data.get("password", None)

        self._account = CustomUserBackend().authenticate(email=email,
                                                         password=password,
                                                         chat_info=self._chat_info,
                                                         is_signin=True)

        if self._account is None:
            raise ValidationError("Password is not match.")

        return data

    def save(self):

        if self._chat_info is None:
            return self._account.get_token().get_res_data()

        else:
            return {"chat_id": self._account.get_chat_info().chat_id,
                    "is_active": self._account.is_active}


class AccountSignUpSerializer(AccountChatAccessSerializer):
    class Meta:
        model = AccountChatAccessSerializer.Meta.model
        fields = AccountChatAccessSerializer.Meta.fields + (
            "email",
            "password",
            "first_name",
            "last_name",
            "language",
        )

    def validate_email(self, value) -> str:
        if Accounts.objects(email=value).first() is not None:
            raise ValidationError("your email is already registered")

        return value


    def validate_password(self, value) -> str:
        email = self.initial_data.get("email", None)

        try:
            validate_password(password=value, user=email)

        except ValidationError as e:
            raise e

        return value


    def validate_first_name(self, value) -> str:
        return capfirst(x=value)


    def validate_last_name(self, value) -> str:
        return capfirst(x=value)


    def validate(self, data:dict) -> dict:
        super(AccountSignUpSerializer, self).validate(data=data)

        chat_id: str = self._chat_info.get("chat_id")
        if ChatInfos.objects(chat_id=chat_id).first() is not None:
            raise ValidationError("You can not create more than 2 accounts in one chat.")

        return data


    def save(self) -> None:
        new_account = Accounts(**self.validated_data)
        new_account.save(**self._chat_info) if self._chat_info is not None else new_account.save()
        return None


### Access w/o activation
class AccountSignOutSerializer(AccountAuthAccessSerializer):
    """
    be advised that this class does not validate chat_info.

    """

    def save(self):
        self._account.signout(token=self._account.get_token() if self._auth_str else None,
                              chat_info=self._account.get_chat_info() if self._chat_info else None)


class AccountActivateSerializer(AccountAuthAccessSerializer):
    def __init__(self, *args, **kwargs):
        self._activation_code = kwargs.pop("activation_code", None)
        super(AccountActivateSerializer, self).__init__(*args, **kwargs)

    def validate(self, data) -> dict:
        super(AccountActivateSerializer, self).validate(data=data)

        if self._account.is_active:
            raise ValidationError("account was already activated.")

        if not self._account.check_activation_code(activation_code=self._activation_code):
            raise ValidationError("invalid activation code.")

        return data

    def save(self):
        self._account.modify(**{"is_active": True})


class SendMailSerializers(AccountAuthAccessSerializer):
    def __init__(self, *args, **kwargs):
        self.__mail_type: str | None = kwargs.pop("mail_type", None)
        super(SendMailSerializers, self).__init__(*args, **kwargs)

    def validate(self, data: dict) -> dict:
        super(SendMailSerializers, self).validate(data=data)

        if self.__mail_type is None:
            raise ValidationError("Bad Request")

        return data

    def save(self) -> None:
        mail_content: dict | None = None

        if self.__mail_type == "activation":
            mail_content: dict = {
                "subject": "[Kryptos] Activation Code for Your Kryptos Account",
                "message": f"""
            Please enter your activation code to activate your Kryptos account.

            ** ACTIVATION CODE: "{self._account.get_activation_code()}"

            From
            Kryptos Administrator
                    """,
                "from_email": "bot@Kryptos_ln.com",
                "recipient_list": [self._account.email],
            }

        if mail_content is not None:
            send_mail(**mail_content)

        return None


### Access w/ activation
class AccountDeleteSerializer(AccountActiveAccessSerializer):
    class Meta:
        model = AccountActiveAccessSerializer.Meta.model
        fields = AccountAuthAccessSerializer.Meta.fields + ("password",)

    def validate(self, data: dict) -> dict:
        super(AccountActiveAccessSerializer, self).validate(data=data)

        password = data.get("password", "")

        if not self._account.check_password(password=password):
            raise ValidationError("password is not match.")

        return data

    def save(self) -> None:
        self._account.delete()


class AccountChangePasswordSerializer(AccountActiveAccessSerializer):
    class Meta:
        model = AccountActiveAccessSerializer.Meta.model
        fields = AccountAuthAccessSerializer.Meta.fields + ("password", )

    def __init__(self, *args, **kwargs):
        self.__new_password = kwargs.pop("new_password", None)
        super(AccountActiveAccessSerializer, self).__init__(*args, **kwargs)

    def validate(self, data:dict) -> dict:
        super(AccountActiveAccessSerializer, self).validate(data=data)

        if not self._account.check_password(password=data.get("password", None)):
            raise ValidationError("current password is not match.")

        try:
            validate_password(password=self.__new_password, user=self._account.email)

        except ValidationError as e:
            raise e

        return data

    def save(self) -> None:
        if self.validated_data.get("password", None) != self.__new_password:
            self._account.modify(**{"password": self.__new_password})
            self._account.save()

        self._account.signout(token=self._account.get_token() if self._auth_str else None,
                              chat_info=self._account.get_chat_info() if self._chat_info else None)
        return None


class AccountGetInfoSerializer(AccountActiveAccessSerializer):
    def save(self):
        return self._account.get_information()


class AccountUpdateSerializer(AccountActiveAccessSerializer):
    class Meta:
        model = AccountActiveAccessSerializer.Meta.model
        fields=  AccountAuthAccessSerializer.Meta.fields + (
            "first_name",
            "last_name",
            "language",
            "max_access_try",
            "visibility"
        )

    def validate_first_name(self, value:str) -> str:
        return capfirst(x=value)

    def validate_last_name(self, value:str) -> str:
        return capfirst(x=value)

    def validate_language(self, value:str) -> str:
        return value

    def validate_max_access_try(self, value:int) -> int:
        return value

    def validate_visibility(self, value:int) -> int:
        return value

    def save(self) -> None:
        for account in  Accounts.objects(**self.validated_data):
            if account == self._account:
                return None

        self._account.modify(**self.validated_data)
        return None


class AccountRegisterLicenseSerializer(AccountActiveAccessSerializer):
    class Meta:
        model = AccountActiveAccessSerializer.Meta.model
        fields=  AccountAuthAccessSerializer.Meta.fields + (
            "license_info",
        )

    def validate_license_info(self, value: dict) -> dict:
        condition1: bool = value.get("kryptos_version", None) == settings.KRYPTOS_VERSION
        condition2: bool = value.get("kryptos_license", None) is not None
        condition3: bool = value.get("kryptos_license_issued", None) is not None
        condition4: bool = value.get("kryptos_license_expire", None) is not None
        condition5: bool = value.get("kryptos_account_email", None) is not None
        condition6: bool = value.get("kryptos_digital_sign", None) == settings.KRYPTOS_DIGITAL_SIGN

        if not condition1 or not condition2 or not condition3 or not condition4 or not condition5 or not condition6:
            raise ValidationError("License is not match with current Kryptos version.")

        return value

    def validate(self, data: dict) -> dict:
        super(AccountRegisterLicenseSerializer, self).validate(data=data)

        if self._account.email != data.get("license_info").get("kryptos_account_email"):
            raise ValidationError("License is not valid for current account.")

        return data

    def save(self) -> None:
        self._account.modify(**self.data)
        return None
