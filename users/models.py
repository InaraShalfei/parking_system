from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MANAGER = 1
    EMPLOYEE = 2

    ROLE_CHOICES = (
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        if self.role is None:
            return False
        if self.role == self.MANAGER:
            return True
        employee_permissions = ['parking_systems.view_parking', 'parking_systems.view_reservation',
                                'parking_systems.add_reservation']
        return perm in employee_permissions
