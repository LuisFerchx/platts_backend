from django.db import models

from apps.authentication.models import User
from config.models import BaseModel


class TypeInvestment(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "type_investment"


# Create your models here.
class Project(BaseModel):
    name = models.CharField(max_length=100)
    type_investment = models.ForeignKey(TypeInvestment, on_delete=models.CASCADE,
                                        related_name='fk_typeinvestment_project')
    dir_real_state = models.CharField(max_length=200, null=True, blank=True)
    total_cost = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)

    class Meta:
        db_table = "project"


class UserProject(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='fk_user_userproject')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, related_name='fk_project_userproject')
    pct_participation = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)

    class Meta:
        db_table = "user_project"
        unique_together = ['user', 'project']


class MaintenanceCosts(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, related_name='fk_project_maintenance')
    json_values = models.TextField(blank=True, null=True)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "maintenance_costs"
