from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

from apps.authentication.models import User
from utils import global_utils


def exist_email(email: str) -> bool:
    if User.objects.filter(email=email).exists():
        return False
    else:
        return True


def verify_email(email: str) -> HttpResponse:
    if exist_email(email):
        return Response(
            global_utils.response_data(message='Email already exist'),
            status=status.HTTP_409_CONFLICT
        )
