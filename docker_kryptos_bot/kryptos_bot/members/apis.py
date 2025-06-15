import requests
from config import KRYPTOS_API_URL, TIMEOUT


KRYPTOS_MEMBER_API_URL: str = f"{KRYPTOS_API_URL}api/v1/accounts/"


def api_activate_account(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}activate/"
    return requests.put(url=url, json=data, timeout=TIMEOUT)


def api_check_chat(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}check_chat/"
    return requests.post(url=url, json=data, timeout=TIMEOUT)


def api_get_user_info(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}info/"
    return requests.get(url=url, json=data, timeout=TIMEOUT)


def api_get_user_activation_info(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}is_active/"
    return requests.get(url=url, json=data, timeout=TIMEOUT)


def api_signin(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}signin/"
    return requests.post(url=url, json=data, timeout=TIMEOUT)


def api_signout(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}signout/"
    return requests.put(url=url, json=data, timeout=TIMEOUT)


def api_signup(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}signup/"
    return requests.post(url=url, json=data, timeout=TIMEOUT)


def api_send_code(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}send_code/"
    return requests.put(url=url, json=data, timeout=TIMEOUT)
