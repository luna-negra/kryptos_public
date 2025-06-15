from rest_framework.decorators import api_view

from .serializers import *
from core import (check_user_request,
                  get_result_from_serializer)


@api_view(["PUT"])
def activate(request):
    """
    activating inactive account. account is required to be signed in.

    :param request:
    :return:
    """
    auth_str, chat_info, res_data, status_code= check_user_request(request=request,
                                                                   msg="activate your account",)

    # get an activation code to activate account.
    activation_code = request.data.pop("activation_code", None)
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=AccountActivateSerializer(data=request.data,
                                                                   chat_info=chat_info,
                                                                   auth_str=auth_str,
                                                                   activation_code=activation_code))


@api_view(["POST"])
def change_pw(request):
    """
    changing password for signed in account info.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="update password")

    # new_password from requester input.
    new_password = request.data.pop("new_password", None)
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=AccountChangePasswordSerializer(data=request.data,
                                                                         auth_str=auth_str,
                                                                         chat_info=chat_info,
                                                                         new_password=new_password))


@api_view(["POST"])
def check_chat(request):
    """
    check the user logged in by SNS.
    Only valid in SNS

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="find account that signed in via chat",
                                                                    auth_status=False)
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=CheckChatInfoSerializer(data=request.data,
                                                                 auth_str=auth_str,
                                                                 chat_info=chat_info))


@api_view(["DELETE"])
def delete(request):
    """
    Delete Account

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="delete an account")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=AccountDeleteSerializer(data=request.data,
                                                                 auth_str=auth_str,
                                                                 chat_info=chat_info))


@api_view(["GET"])
def get_info(request):
    """
    getting signed in account info.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="get an account information")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=AccountGetInfoSerializer(data=request.data,
                                                                  auth_str=auth_str,
                                                                  chat_info=chat_info,
                                                                  partial=True))


@api_view(["GET"])
def is_active(request):
    """
    check the user is in active status or not

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="get an activation status for user.")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=AccountGetActivationInfoSerializer(data=request.data,
                                                                            auth_str=auth_str,
                                                                            chat_info=chat_info,
                                                                            partial=True))


@api_view(["POST"])
def register_license(request):
    """
    registering personal license information.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="get an account information")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=AccountRegisterLicenseSerializer(data=request.data,
                                                                          auth_str=auth_str,
                                                                          chat_info=chat_info,
                                                                          partial=True))


@api_view(["PUT"])
def send_activation_code(request):
    """
    sending email with activation code.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="send activation code")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=SendMailSerializers(data=request.data,
                                                             auth_str=auth_str,
                                                             chat_info=chat_info,
                                                             mail_type="activation"))


@api_view(["POST"])
def signup(request):
    """
    creating new account.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="create a new account")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=AccountSignUpSerializer(data=request.data,
                                                                 chat_info=chat_info,
                                                                 auth_str=auth_str))


@api_view(["POST"])
def signin(request):
    """
    authenticating account.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="sign in",
                                                                    auth_status=False)
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=AccountSignInSerializer(data=request.data,
                                                                 chat_info=chat_info,
                                                                 auth_str=auth_str))


@api_view(["PUT"])
def signout(request):
    """
    signing out account.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="sign out")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=AccountSignOutSerializer(data=request.data,
                                                                  auth_str=auth_str,
                                                                  chat_info=chat_info))


@api_view(["PATCH"])
def update(request):
    """
    updating signed in account.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="update account information")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=AccountUpdateSerializer(data=request.data,
                                                                 auth_str=auth_str,
                                                                 chat_info=chat_info,
                                                                 partial=True, ))
