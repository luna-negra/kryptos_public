from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.authentication import BaseAuthentication
from .models import (Accounts,
                     Tokens,
                     check_password,
                     datetime, ChatInfos, )


class CustomUserBackend(BaseAuthentication):

    def authenticate(self, *args, **kwargs) -> Accounts | None:
        email = kwargs.get("email", None)
        password = kwargs.get("password", None)
        chat_info = kwargs.get("chat_info")
        is_signin = kwargs.get("is_signin", None)
        account = Accounts.objects(email=email).first()
        update_data: dict = {}

        if account is not None:

            if check_password(password=password, encoded=account.password):
                update_data.update({"consecutive_access_fail": 0})

                if is_signin:
                    update_data.update({"last_access_datetime": datetime.now()})

                    if chat_info:
                        prev_chat_info = account.get_chat_info()

                        if prev_chat_info is None:
                            ChatInfos(uuid=account.uuid,
                                      msg_name=chat_info.get("msg_name", None),
                                      chat_id=chat_info.get("chat_id", None)).save()

                        else:
                            if prev_chat_info != ChatInfos.objects(uuid=account.uuid, **chat_info).first():
                                account.change_code()
                                update_data.update({"is_active": False})
                                chat_info.update({"is_signed_in": True})
                                prev_chat_info.modify(**chat_info)

                            else:
                                prev_chat_info.modify(**{"is_signed_in": True})

                    else:
                        self.create_token(account=account)

                    account.modify(signin=True, **update_data)
                return account

            else:
                if account.is_active:
                    update_data.update({"consecutive_access_fail": account.consecutive_access_fail + 1})

                    if account.max_access_try == account.consecutive_access_fail + 1:
                        update_data.update({"is_active": False})
                        account.change_code()

                    account.update(**update_data)

        return None


    def create_token(self, account) -> None:
        new_token = RefreshToken.for_user(user=account).access_token

        while True:
            access_token = str(new_token)
            if Tokens.objects(token=access_token).first() is None:
                break

            new_token = RefreshToken.for_user(user=account).access_token

        # set issue_date of token
        issued_date = datetime.now()

        # update token information
        token = account.get_token()
        token.token = access_token
        token.issued_datetime = issued_date
        token.expire_datetime = issued_date + new_token.lifetime
        token.save()
        return None
