from django.urls import path
from .views import *


app_name: str = "documents"
urlpatterns: list = [
    path("", get_bulk_doc, name="get_list"),
    path("delete/", delete_bulk_doc, name="delete_list"),
    path("statistics/", get_statistics, name="get_statistics"),

    path("create/", create_doc, name="create"),
    path("<str:uuid>/", get_doc, name="get"),
    path("<str:uuid>/delete/", delete_doc, name="delete"),
    path("<str:uuid>/change_pw/", change_doc_pw, name="change_pw"),
    path("<str:uuid>/update/", update_doc, name="update"),

]
