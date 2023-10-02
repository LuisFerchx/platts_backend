from rest_framework import serializers

from apps.projects.models import UserProject


class UserProjectDetails_serializer(serializers.ModelSerializer):
    user_code = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    project_code = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    pct_participation = serializers.SerializerMethodField()
    usd_total = serializers.SerializerMethodField()

    class Meta:
        model = UserProject
        fields = (
            'user_code', 'user_name', 'project_code', 'project_name', 'total_cost', 'pct_participation', 'usd_total',
            'pct_participation')

    def get_user_code(self, obj):
        return obj.user.code

    def get_user_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def get_project_code(self, obj):
        return obj.project.code

    def get_project_name(self, obj):
        return obj.project.name

    def get_pct_participation(self, obj):
        return round(obj.pct_participation, 2)

    def get_total_cost(self, obj):
        return round(obj.project.total_cost, 2)

    def get_usd_total(self, obj):
        total = obj.project.total_cost * obj.pct_participation/100
        return round(total, 2)
