from django.db import models

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

    class Meta:
        db_table = "project"
