import traceback

from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.models import User
from apps.projects.models import Project, TypeInvestment, UserProject
from apps.projects.serializers import UserProjectDetails_serializer
from utils import global_utils
from utils.encryption_util import EncryptDES
from utils.vars import HttpMessages

_e = EncryptDES()


# Create your views here.
class Project_ViewSet(viewsets.ViewSet):
    queryset = Project.objects.none()

    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            obj_proj = Project.objects.filter(state=1).values('code', 'name', 'dir_real_state', 'total_cost',
                                                              'type_investment__name')
            return Response(
                global_utils.response_data(data={"projects": obj_proj}),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                global_utils.response_data(message=HttpMessages.list_error, data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request):
        try:
            data = request.data

            with transaction.atomic():
                obj_project = Project()
                obj_project.name = data.get('name')
                obj_project.dir_real_state = data.get('dir_real_state')
                obj_project.total_cost = data.get('total_cost')
                obj_project.type_investment_id = TypeInvestment.objects.get(
                    pk=_e.decrypt(data.get('type_investment_code'))).pk
                obj_project.save()

                obj_project.code = _e.encrypt(obj_project.pk)
                obj_project.save()

            return Response(
                global_utils.response_data(data={"project_code": obj_project.code},
                                           message=HttpMessages.success_created),
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                global_utils.response_data(message=HttpMessages.error_created, data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        try:
            data = request.data
            with transaction.atomic():
                obj_proj = Project.objects.get(code=pk, state=1)
                obj_proj.name = data.get('name')
                obj_proj.dir_real_state = data.get('dir_real_state')
                obj_proj.total_cost = data.get('total_cost')
                obj_proj.type_investment_id = TypeInvestment.objects.get(
                    pk=_e.decrypt(data.get('type_investment_code'))).pk
                obj_proj.save()

            return Response(
                global_utils.response_data(data={"project_code": obj_proj.code},
                                           message=HttpMessages.update_success),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                global_utils.response_data(message=HttpMessages.update_error, data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    #
    def retrieve(self, request, pk):
        try:
            obj_proj = Project.objects.get(code=pk, state=1)

            json_data = {
                "name": obj_proj.name,
                "code": obj_proj.code,
                "dir_real_state": obj_proj.dir_real_state,
                "total_cost": obj_proj.total_cost,
                "type_investment": obj_proj.type_investment.name
            }

            return Response(
                global_utils.response_data(data=json_data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                global_utils.response_data(message='Error when get Project', data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        try:
            flag = False
            with transaction.atomic():
                obj_proj = Project.objects.filter(code=pk, state=1)
                if obj_proj.exists():
                    msg_details = obj_proj.delete()
                else:
                    return Response(global_utils.response_data('No Data Found'),
                                    status=status.HTTP_400_BAD_REQUEST)
                total_depends = int(msg_details[0])
                if total_depends > 1:
                    flag = True
                raise Exception(flag)
        except Exception as e:
            if str(e) == 'False':
                obj_user = Project.objects.get(code=pk, state=1)
                obj_user.state = 0
                obj_user.save()

                return Response(global_utils.response_data(message=HttpMessages.delete_success, data=msg_details),
                                status=status.HTTP_200_OK)
            else:
                traceback.print_exc()
                return Response(global_utils.response_data(HttpMessages.delete_error + ': ' + str(e)),
                                status=status.HTTP_400_BAD_REQUEST)


class TypeInvestment_ViewSet(viewsets.ViewSet):
    queryset = TypeInvestment.objects.none()

    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            obj = TypeInvestment.objects.filter(state=1).values('code', 'name')
            return Response(
                global_utils.response_data(data={"Investments": obj}),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                global_utils.response_data(message=HttpMessages.list_error, data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request):
        try:
            data = request.data

            with transaction.atomic():
                obj = TypeInvestment()
                obj.name = data.get('name')
                obj.save()

                obj.code = _e.encrypt(obj.pk)
                obj.save()

            return Response(
                global_utils.response_data(data={"type_investment_code": obj.code},
                                           message=HttpMessages.success_created),
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                global_utils.response_data(message=HttpMessages.error_created, data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):
        try:
            data = request.data
            with transaction.atomic():
                obj = TypeInvestment.objects.get(code=pk, state=1)
                obj.name = data.get('name')
                obj.save()

            return Response(
                global_utils.response_data(data={"type_investment_code": obj.code},
                                           message=HttpMessages.update_success),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                global_utils.response_data(message=HttpMessages.update_error, data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    #
    def retrieve(self, request, pk):
        try:
            obj = TypeInvestment.objects.get(code=pk, state=1)

            json_data = {
                "name": obj.name,
                "code": obj.code,
            }

            return Response(
                global_utils.response_data(data=json_data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                global_utils.response_data(message='Error when get Investment', data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):
        try:
            flag = False
            with transaction.atomic():
                obj = TypeInvestment.objects.filter(code=pk, state=1)
                if obj.exists():
                    msg_details = obj.delete()
                else:
                    return Response(global_utils.response_data('No Data Found'),
                                    status=status.HTTP_400_BAD_REQUEST)
                total_depends = int(msg_details[0])
                if total_depends > 1:
                    flag = True
                raise Exception(flag)
        except Exception as e:
            if str(e) == 'False':
                obj_user = TypeInvestment.objects.get(code=pk, state=1)
                obj_user.state = 0
                obj_user.save()

                return Response(global_utils.response_data(message=HttpMessages.delete_success, data=msg_details),
                                status=status.HTTP_200_OK)
            else:
                traceback.print_exc()
                return Response(global_utils.response_data(HttpMessages.delete_error + ': ' + str(e)),
                                status=status.HTTP_400_BAD_REQUEST)


class ProjectUser_ViewSet(viewsets.ViewSet):
    queryset = Project.objects.none()

    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            data = request.data
            # Para el administrador
            with transaction.atomic():
                obj = UserProject()
                obj.user_id = User.objects.get(code=data.get('user_code'), state=1).pk
                obj.project_id = Project.objects.get(code=data.get('project_code')).pk
                obj.pct_participation = data.get('pct_participation')
                obj.save()

                return Response(
                    global_utils.response_data(data={
                        "client_projects": UserProject.objects.filter(user_id=obj.user_id, state=1).values(
                            'project__code',
                            'project__name')},
                        message="Project add to Client"),
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            return Response(
                global_utils.response_data(message=HttpMessages.error_created, data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request):
        data = request.GET
        try:
            obj = UserProject.objects.filter(state=1)
            if data.get('user_code'):
                user = User.objects.get(code=data.get('user_code'), state=1)
                obj = UserProject.objects.filter(user_id=user.pk)

            return Response(
                global_utils.response_data(data=UserProjectDetails_serializer(obj, many=True).data,
                                           message="Details"),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                global_utils.response_data(message=HttpMessages.list_error, data=str(e)),
                status=status.HTTP_400_BAD_REQUEST
            )

# class ProjectUserDelete_ViewSet(viewsets.ViewSet):
#     queryset = Project.objects.none()
#
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request):
#         try:
#             data = request.data
#             # Para el administrador
#             with transaction.atomic():
#                 obj = UserProject()
#                 obj.user_id = User.objects.get(code=data.get('user_code')).pk
#                 obj.project_id = Project.objects.get(code=data.get('project_code')).pk
#                 obj.pct_participation = data.get('pct_participation')
#                 obj.save()
#
#                 return Response(
#                     global_utils.response_data(data={
#                         "client_projects": UserProject.objects.filter(user_id=obj.user_id).values('project__code',
#                                                                                                   'project__name')},
#                         message="Project add to Client"),
#                     status=status.HTTP_201_CREATED
#                 )
#         except Exception as e:
#             return Response(
#                 global_utils.response_data(message=HttpMessages.error_created, data=str(e)),
#                 status=status.HTTP_400_BAD_REQUEST
#             )
