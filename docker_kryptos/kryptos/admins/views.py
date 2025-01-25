from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK,
                                   HTTP_201_CREATED,
                                   HTTP_202_ACCEPTED,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED,
                                   HTTP_403_FORBIDDEN,
                                   )


# Create your views here.

@api_view(["GET"])
def health_check(request):
    res_data = {
        "result": True,
        "msg": "You can use Kryptos API without errors."
    }
    status_code = HTTP_200_OK

    return Response(status=status_code, data=res_data)


class AccountsListView(APIView):
    def get(self, request):
        """
        for getting list of accounts related with signed in account.

        :param request:
        :return:
        """
        return Response(status=status_code, data=res_data)


    def post(self, request):
        """
        for updating bulk accounts related with signed in account.

        :param request:
        :return:
        """
        return Response(status=status_code, data=res_data)