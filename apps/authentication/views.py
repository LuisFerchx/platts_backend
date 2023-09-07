from datetime import timedelta

from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.models import User
from apps.authentication.serializers import UserSerializer


class UserLoginView(APIView):
    def post(self, request):
        data = request.data

        email = data.get('email')
        pwd = data.get('password')
        user = authenticate(request, username=email, password=pwd)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            refresh.set_exp(lifetime=timedelta(days=30))
            access_token = refresh.access_token

            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(access_token),
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response('No User Exist', status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(GenericAPIView):
    def post(self, request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({'error': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh_token = RefreshToken(refresh)
            refresh_token.set_exp(lifetime=timedelta(days=30))
            access_token = refresh_token.access_token

            return Response(
                {
                    'refresh': str(refresh_token),
                    'access': str(access_token),
                }, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({'error': 'Invalid refresh token. ', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)