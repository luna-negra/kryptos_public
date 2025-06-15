import requests
from config import TIMEOUT
from members.apis import KRYPTOS_MEMBER_API_URL


def api_delete_kryptos_account(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}delete/"
    return requests.delete(url=url, json=data, timeout=TIMEOUT)


def api_update_user_info(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}update/"
    return requests.patch(url=url, json=data, timeout=TIMEOUT)


def api_update_password(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}change_pw/"
    return requests.post(url=url, json=data, timeout=TIMEOUT)


def api_register_license(data:dict):
    url: str = f"{KRYPTOS_MEMBER_API_URL}license/"
    return requests.post(url=url, json=data, timeout=TIMEOUT)
