import traceback
from datetime import timedelta

from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication import utils
from apps.authentication.models import User
from apps.authentication.serializers import UserSerializer
from utils import global_utils
from utils.encryption_util import EncryptDES

_e = EncryptDES()


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


class UserProfile_ViewSet(viewsets.ViewSet):
    queryset = User.objects.none()

    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            data = request.data
            utils.verify_email(data['email'])
            with transaction.atomic():
                obj_user = User()
                obj_user.username = data['username']
                obj_user.first_name = data['first_name']
                obj_user.last_name = data['last_name']
                obj_user.identification = data['identification']
                obj_user.phone = data['phone']
                obj_user.birth_date = data['birth_date']
                obj_user.direction = data['direction']
                obj_user.tip_ident = data['tip_ident']
                obj_user.email = data['email']
                obj_user.is_superuser = True if data['is_admin'] == 1 else False
                obj_user.is_active = 0 if data['is_admin'] == 0 else 1
                obj_user.set_password(data['password'])
                obj_user.save()

                obj_user.code = _e.encrypt(obj_user.pk)
                obj_user.save()

            return Response(
                global_utils.response_data(data={"user_code": obj_user.code}, message="User Created Success"),
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                global_utils.response_data(message='Error when create user', data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        try:
            data = request.data
            with transaction.atomic():
                obj_user = User.objects.get(code=pk, state=1)

                if obj_user.email != data['email']:
                    utils.verify_email(data['email'])

                obj_user.username = data['username']
                obj_user.first_name = data['first_name']
                obj_user.last_name = data['last_name']
                obj_user.identification = data['identification']
                obj_user.phone = data['phone']
                obj_user.birth_date = data['birth_date']
                obj_user.direction = data['direction']
                obj_user.tip_ident = data['tip_ident']
                obj_user.email = data['email']
                obj_user.is_superuser = True if data['is_admin'] == 1 else False
                obj_user.set_password(data['password'])
                obj_user.save()

            return Response(
                global_utils.response_data(data={"user_code": obj_user.code}, message="User Update Success"),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                global_utils.response_data(message='Error when create user', data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk):
        try:
            obj_user = User.objects.get(code=pk, state=1)

            json_data = {
                "username": obj_user.username,
                "code": obj_user.code,
                "first_name": obj_user.first_name,
                "last_name": obj_user.last_name,
                "tip_ident": obj_user.tip_ident,
                "identification": obj_user.identification,
                "direction": obj_user.direction,
                "phone": obj_user.phone,
                "birth_date": obj_user.birth_date,
                "is_admin": obj_user.is_superuser,
            }

            return Response(
                global_utils.response_data(data=json_data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                global_utils.response_data(message='Error when get user', data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        try:
            flag = False
            with transaction.atomic():
                insp_obj = User.objects.filter(code=pk, state=1)
                if insp_obj.exists():
                    msg_details = insp_obj.delete()
                else:
                    return Response(global_utils.response_data('No Data Found'),
                                    status=status.HTTP_400_BAD_REQUEST)
                total_depends = int(msg_details[0])
                if total_depends > 1:
                    flag = True
                raise Exception(flag)
        except Exception as e:
            print(e)
            if str(e) == 'False':
                obj_user = User.objects.get(code=pk, state=1)
                obj_user.state = 0
                obj_user.save()

                return Response(global_utils.response_data(message='User Deleted', data=msg_details),
                                status=status.HTTP_200_OK)
            else:
                traceback.print_exc()
                return Response(global_utils.response_data('Error when delete: ' + str(e)),
                                status=status.HTTP_400_BAD_REQUEST)
