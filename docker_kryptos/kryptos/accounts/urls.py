from django.urls import path
from .views import *


app_name: str = "accounts"
urlpatterns: list = [
    path("activate/", activate, name="validate"),
    path("change_pw/", change_pw, name="change_pw"),
    path("check_chat/", check_chat, name="check_chat"),
    path("delete/", delete, name="delete"),
    path("info/", get_info, name="info"),
    path("is_active/", is_active, name="is_active"),
    path("license/", register_license, name="set_license"),
    path("send_code/", send_activation_code, name="send_mail"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("signup/", signup, name="signup"),
    path("update/", update, name="update"),
]
