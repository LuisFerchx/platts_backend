from django.urls import re_path, include
from rest_framework import routers

from apps.authentication.views import UserProfile_ViewSet

router = routers.DefaultRouter()
router.register(r"user", UserProfile_ViewSet)

urlpatterns = [
    re_path(r"", include(router.urls)),
]
