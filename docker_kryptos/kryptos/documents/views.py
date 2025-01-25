from rest_framework.decorators import api_view

from .serializers import *
from core import (check_user_request,
                  get_result_from_serializer,)


@api_view(["POST"])
def create_doc(request):
    """
    creating new document for signin user.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="create a new document")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=DocumentCreateSerializer(data=request.data,
                                                                  auth_str=auth_str,
                                                                  chat_info=chat_info))


@api_view(["PUT"])
def change_doc_pw(request, uuid):
    """
    changing password in a specific document.

    :param request:
    :param uuid:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="change password in a document")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=DocumentPasswordUpdateSerializer(data=request.data,
                                                                          auth_str=auth_str,
                                                                          chat_info=chat_info,
                                                                          uuid=uuid))


@api_view(["DELETE"])
def delete_doc(request, uuid):
    """
    Deleting a document information with specific ID.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="delete a document")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=DocumentDeleteSerializer(data=request.data,
                                                                  auth_str=auth_str,
                                                                  chat_info=chat_info,
                                                                  uuid=uuid))


@api_view(["DELETE"])
def delete_bulk_doc(request):
    """
    delete documents with doc_uuid.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="delete docs in bulk")

    # docs uuid list input by requester
    docs_uuid_list = request.data.pop("docs_uuid_list", None)
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=DocumentsListDeleteSerializer(data=request.data,
                                                                       auth_str=auth_str,
                                                                       chat_info=chat_info,
                                                                       docs_uuid_list=docs_uuid_list))



@api_view(["GET"])
def get_doc(request, uuid):
    """
    getting a document information with specific ID.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="get a document information")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=DocumentGetInfoSerializer(data=request.data,
                                                                   auth_str=auth_str,
                                                                   chat_info=chat_info,
                                                                   uuid=uuid))


@api_view(["GET"])
def get_bulk_doc(request):
    """
    getting documents with search query.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="search docs information")

    #search query input by requester
    search_q = { k:v[0] for k,v in dict(request.GET).items() }
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=DocumentsListGetInfoSerializer(data=request.data,
                                                                        auth_str=auth_str,
                                                                        chat_info=chat_info,
                                                                        search_q=search_q,
                                                                        partial=True))


@api_view(["GET"])
def get_statistics(request):
    """
    getting statistics information for stored documents.

    :param request:
    :return:
    """
    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="search docs information")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=DocumentsStatisticsSerializer(data=request.data,
                                                                        auth_str=auth_str,
                                                                        chat_info=chat_info))


@api_view(["PUT"])
def update_doc(request, uuid):
    """
    updating an information of specific document.

    :param request:
    :return:
    """

    auth_str, chat_info, res_data, status_code = check_user_request(request=request,
                                                                    msg="get a document information")
    return get_result_from_serializer(status_code=status_code,
                                      res_data=res_data,
                                      sr=DocumentUpdateSerializer(data=request.data,
                                                                  auth_str=auth_str,
                                                                  chat_info=chat_info,
                                                                  uuid=uuid,
                                                                  partial=True))
