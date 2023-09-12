"""
URL configuration for config project.

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
from django.contrib import admin
from django.urls import path, re_path, include

from apps.authentication.views import UserLoginView, RefreshTokenView, UserLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"api/", include("apps.authentication.urls")),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('api/logout/', UserLogoutView.as_view(), name='user-logout'),
    path('api/refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
]
