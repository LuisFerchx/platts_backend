from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    code = models.CharField(null=True, blank=True)
    identification = models.CharField(max_length=20, null=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    direction = models.CharField(max_length=200, null=True, blank=True)
    tip_ident = models.CharField(max_length=2, null=True, blank=True)
    state = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        unique_together = ['email']


class Adm_Rol(models.Model):
    name = models.CharField(max_length=50)
    is_admin = models.SmallIntegerField(default=0)
    state = models.SmallIntegerField(default=1)

    class Meta:
        db_table = "adm_rol"
