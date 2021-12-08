from datetime import datetime

from django.db import models


class Parking(models.Model):
    number = models.IntegerField(primary_key=True, unique=True, verbose_name='Номер парковочного места')

    def __str__(self):
        return f'Парковочное место № {self.number}'


class Reservation(models.Model):
    parking_space = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='reservations',
                                      verbose_name='Номер парковочного места')
    start_time = models.DateTimeField(verbose_name='Время начала брони')
    finish_time = models.DateTimeField(verbose_name='Время окончания брони')

    class Meta:
        ordering = ['parking_space']
        constraints = [
            models.UniqueConstraint(fields=['parking_space', 'start_time'], name='unique_reservation')
        ]
