from mizuhara.core.routes import (connector_callback,
                                  connector_command,
                                  connector_message,)

from managements.views import *


# Mapping handlers and views for Telegram Bot commands.
COMMANDS: list = [
    connector_command(view=management, commands=["management"]),
    connector_command(view=search_docs, commands=["search_account"]),
]


MESSAGES: list = [
    connector_message(view=edit_doc_with_description, allowed_pre_route=["edit_doc_with_description"]),
    connector_message(view=edit_doc_with_password, allowed_pre_route=["edit_doc_with_password"]),
    connector_message(view=edit_doc_with_site, allowed_pre_route=["edit_doc_with_site"]),
    connector_message(view=edit_doc_with_username, allowed_pre_route=["edit_doc_with_username"]),
    connector_message(view=register_new_doc, allowed_pre_route=["register_new_doc"]),
    connector_message(view=search_docs_with_url, allowed_pre_route=["search_docs_with_url"]),
    connector_message(view=search_docs_with_description, allowed_pre_route=["search_docs_with_description"]),
]


CALLBACKS: list = [
    connector_callback(view=delete_doc,
                       callback_data=["delete_doc"],
                       allowed_pre_route=["show_doc_info"]),
    connector_callback(view=edit_doc,
                       callback_data=["edit_doc"],
                       allowed_pre_route=["show_doc_info",
                                          "edit_doc_with_description",
                                          "edit_doc_with_password",
                                          "edit_doc_with_site",
                                          "edit_doc_with_username"]),

    connector_callback(view=edit_doc_with_description,
                       callback_data=["edit_doc_with_description"],
                       allowed_pre_route=["edit_doc"]),
    connector_callback(view=edit_doc_with_password,
                       callback_data=["edit_doc_with_password"],
                       allowed_pre_route=["edit_doc"]),
    connector_callback(view=edit_doc_with_site,
                       callback_data=["edit_doc_with_site"],
                       allowed_pre_route=["edit_doc"]),
    connector_callback(view=edit_doc_with_username,
                       callback_data=["edit_doc_with_username"],
                       allowed_pre_route=["edit_doc"]),

    connector_callback(view=management,
                       callback_data=["management"],
                       allowed_pre_route=["main_member", "register_new_doc", "search_docs", "statistics"]),
    connector_callback(view=register_new_doc,
                       callback_data=["register_new_doc"],
                       allowed_pre_route=["management", "register_new_doc"]),
    connector_callback(view=search_docs,
                       callback_data=["search_docs"],
                       allowed_pre_route=["delete_doc",
                                          "edit_doc",
                                          "management",
                                          "search_all_docs",
                                          "search_docs_with_url",
                                          "search_docs_with_description",
                                          "show_search_result_list",
                                          "show_doc_info"]),
    connector_callback(view=search_all_docs,
                       callback_data=["search_all_docs"],
                       allowed_pre_route=["search_docs"],
                       ),
    connector_callback(view=search_docs_with_url,
                       callback_data=["search_docs_with_url"],
                       allowed_pre_route=["search_docs"]),
    connector_callback(view=search_docs_with_description,
                       callback_data=["search_docs_with_description"],
                       allowed_pre_route=["search_docs"]),
    connector_callback(view=show_search_result_list,
                       callback_data=["show_search_result_list"],
                       allowed_pre_route=["show_search_result_list"]),
    connector_callback(view=show_doc_info,
                       allowed_pre_route=["show_search_result_list"]),
    connector_callback(view=statistics,
                       callback_data=["statistics"],
                       allowed_pre_route=["management"]),
]

