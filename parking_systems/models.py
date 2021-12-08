from django.db import models


class Parking(models.Model):

    def __str__(self):
        return f'Парковочное место № {self.id}'


class Reservation(models.Model):
    parking_space = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='reservations',
                                      verbose_name='Номер парковочного места')
    start_time = models.DateTimeField(verbose_name='Время начала брони')
    finish_time = models.DateTimeField(verbose_name='Время окончания брони')

    class Meta:
        ordering = ['parking_space']

    def __str__(self):
        return f'Бронирование № {self.id}'
