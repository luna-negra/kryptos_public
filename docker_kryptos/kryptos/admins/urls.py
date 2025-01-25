from django.urls import path
from .views import *


app_name: str = "admins"
urlpatterns: list = [
    path("accounts/", AccountsListView.as_view(), name="accounts"),
    path("accounts/bulk_update/", AccountsListView.as_view(), name="bulk_update"),
]