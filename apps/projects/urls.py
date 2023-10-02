from django.urls import re_path, include
from rest_framework import routers

from apps.projects.views import Project_ViewSet, TypeInvestment_ViewSet, ProjectUser_ViewSet

router = routers.DefaultRouter()
router.register(r"project", Project_ViewSet)
router.register(r"investment", TypeInvestment_ViewSet)
router.register(r"user_project", ProjectUser_ViewSet)

urlpatterns = [
    re_path(r"", include(router.urls)),
]
