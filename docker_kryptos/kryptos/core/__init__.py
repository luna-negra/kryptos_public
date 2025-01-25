from socket import (gethostbyaddr,
                    herror,)
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED)


def check_user_request(request, msg:str, auth_status:bool=True):
    """
    getting a request and returning authorization string, messenger info, response data and status code.

    :param auth_status:
    :param request: request
    :param msg: set the basic text in data.msg
    :return:
    """

    # template of response data
    res_data: dict = {
        "result": False,
        "msg": f"fail to {msg}.",
    }

    # check the requester's access IP with port. (PROTOCOL://IP:PORT)
    try:
        remote_host = gethostbyaddr(request.META.get("REMOTE_ADDR"))[0].split(".")[0].replace("_", "-")
    except herror:
        remote_host = request.META.get("REMOTE_ADDR")

    # get an authorization string.
    auth_str = request.headers.get("Authorization", None)
    auth_str = auth_str.replace("Bearer ", "") if auth_str else None

    # get a chat information from sns access requester
    chat_info = request.data.pop("chat_info", None) if settings.BOT_HOSTNAME in remote_host else None

    # decide default status code
    if auth_status and auth_str is None and chat_info is None:
        status_code = HTTP_401_UNAUTHORIZED
    else:
        status_code = HTTP_400_BAD_REQUEST

    return auth_str, chat_info, res_data, status_code


def get_result_from_serializer(sr, status_code, res_data:dict):
    if sr.is_valid():
        result = sr.save()
        if result is not None:
            res_data["info"] = result

        res_data["result"] = True
        res_data["msg"] = res_data["msg"].replace("fail", "success")
        status_code = HTTP_200_OK

    else:
        res_data["errors"] = sr.errors

    return Response(status=status_code, data=res_data)
