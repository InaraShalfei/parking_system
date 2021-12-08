from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    Manager = 1
    Employee = 2
    ROLE_CHOICES = (
        (Manager, 'Manager'),
        (Employee, 'Employee')
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
