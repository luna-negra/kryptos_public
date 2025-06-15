from execute import bot
# do not edit above this line.
# please write down your code below.

from managements.serializers import *
from members.views import main, check_signin


async def delete_doc(types):
    sr = DeleteDoc(types=types, route="delete_doc")
    await sr.send_message()
    await search_docs(types=types)
    return None


async def edit_doc(types):
    sr = EditDoc(types=types, route="edit_doc", row_width=1)
    if not await sr.pre_process():
        await show_doc_info(types=types)
        return None

    await sr.send_message()
    return None


async def edit_doc_with_description(types):
    sr = EditDocWithDescription(types=types, route="edit_doc_with_description", link_route="edit_doc")
    if await sr.get_client_data():
        await edit_doc(types=types)
    return None


async def edit_doc_with_password(types):
    sr = EditDocWithPassword(types=types, route="edit_doc_with_password", link_route="edit_doc")
    if await sr.get_client_data():
        await edit_doc(types=types)
    return None


async def edit_doc_with_site(types):
    sr = EditDocWithSite(types=types, route="edit_doc_with_site", link_route="edit_doc")
    if await sr.get_client_data():
        await edit_doc(types=types)
    return None


async def edit_doc_with_username(types):
    sr = EditDocUsername(types=types, route="edit_doc_with_username", link_route="edit_doc")
    if await sr.get_client_data():
        await edit_doc(types=types)
    return None


async def management(types):
    if await check_signin(types=types):
        sr = Management(types=types, route="management", row_width=1)
        await sr.send_message()
        return None

    await main(types=types)
    return None


async def register_new_doc(types):
    sr = RegisterNewDoc(types=types, route="register_new_doc", link_route="management")
    if not await sr.pre_process():
        await sr.send_message()
        await management(types=types)
        return None

    if await sr.get_client_data():
        await management(types=types)
    return None


async def search_docs(types):
    if await check_signin(types=types):
        sr = SearchDocs(types=types, route="search_docs", row_width=1)
        await sr.send_message()
        return None

    await main(types=types)
    return None


async def search_all_docs(types):
    sr = SearchAllDocs(types=types, route="search_all_docs")
    if await sr.send_message():
        await show_search_result_list(types=types)
    return None


async def search_docs_with_url(types):
    sr = SearchDocsWithURL(types=types, route="search_docs_with_url", link_route="search_docs")
    if await sr.get_client_data():
        await show_search_result_list(types=types)
    return None


async def search_docs_with_description(types):
    sr = SearchAccountsWithDescription(types=types, route="search_docs_with_description", link_route="search_docs")
    if await sr.get_client_data():
        await show_search_result_list(types=types)
    return None


async def show_search_result_list(types):
    sr = SearchResult(types=types,
                      route="show_search_result_list",
                      basic_route="show_search_result_list",
                      parent_route="search_docs",
                      row_width=1,
                      num_in_page=5)
    if not await sr.send_message():
        await search_docs(types=types)
    return None


async def show_doc_info(types):
    sr = ShowDocInfo(types=types, route="show_doc_info", row_width=1)
    await sr.send_message()
    return None


async def statistics(types):
    sr = Statistics(types=types, route="statistics", link_route="management")
    await sr.send_message()
    return None
