"""
URL configuration for cryptex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from accounts import urls as urls_accounts
from admins import urls as urls_admins
from documents import urls as urls_documents
from admins.views import health_check


URL_HEADER: str = "api/v1/"
urlpatterns = [
    path(f"{URL_HEADER}", health_check, name="health_check"),
    path(f"{URL_HEADER}accounts/", include(urls_accounts)),
    path(f"{URL_HEADER}admins/", include(urls_admins)),
    path(f"{URL_HEADER}documents/", include(urls_documents)),
]
