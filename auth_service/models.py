from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    invite_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name



class User(AbstractUser):
    email = models.EmailField(unique=True)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='auth_service_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='auth_service_user_set',
        blank=True
    )


