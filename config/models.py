from django.db import models


# Clase base para extender funcionalidades
class BaseModel(models.Model):
    code = models.CharField(max_length=25, blank=True, null=True)
    state = models.SmallIntegerField(default=1)

    class Meta:
        abstract = True
