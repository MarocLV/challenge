from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid


class Roles(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"

class CustomUser(AbstractUser):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    username = models.CharField(max_length=50, unique=True)
    role = models.ForeignKey(Roles, null=True, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=40, unique=True)
    description = models.TextField(max_length=100, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return f"{self.id} - {self.username} - {self.role} - {self.email} - {self.description}"


class HitmanProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    supervisor = models.ForeignKey(
                 CustomUser,
                 null=True,
                 blank=True,
                 on_delete=models.DO_NOTHING,
                 related_name='Supervisor')  
    def __str__(self):
        return f"{self.user} - {self.supervisor}"