import requests
from config import KRYPTOS_API_URL, TIMEOUT


KRYPTOS_DOCUMENT_API_URL: str = f"{KRYPTOS_API_URL}api/v1/documents/"


def api_delete_doc(data:dict, uuid: str):
    url = f"{KRYPTOS_DOCUMENT_API_URL}{uuid}/delete/"
    return requests.delete(url=url, json=data, timeout=TIMEOUT)


def api_doc_change_password(data:dict, uuid:str):
    url = f"{KRYPTOS_DOCUMENT_API_URL}{uuid}/change_pw/"
    return requests.put(url=url, json=data, timeout=TIMEOUT)


def api_get_doc_with_uuid(data:dict, uuid: str):
    url = f"{KRYPTOS_DOCUMENT_API_URL}{uuid}/"
    return requests.get(url=url, json=data, timeout=TIMEOUT)


def api_get_statistics(data:dict):
    url = f"{KRYPTOS_DOCUMENT_API_URL}statistics/"
    return requests.get(url=url, json=data, timeout=TIMEOUT)


def api_register_new_doc(data:dict):
    url = f"{KRYPTOS_DOCUMENT_API_URL}create/"
    return requests.post(url=url, json=data, timeout=TIMEOUT)


def api_search_docs(data:dict):
    url = f"{KRYPTOS_DOCUMENT_API_URL}?"

    if data.get("search_q", None) is not None:
        for k, v in data.pop("search_q").items():
            url += f"{k}={v.lower()}&"

    url = url[:-1]
    return requests.get(url=url, json=data, timeout=TIMEOUT)


def api_update_doc(data:dict, uuid: str):
    url = f"{KRYPTOS_DOCUMENT_API_URL}{uuid}/update/"
    return requests.put(url=url, json=data, timeout=TIMEOUT)
