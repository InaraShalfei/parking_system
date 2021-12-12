from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils import timezone

from parking_systems.models import Reservation


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

    def __init__(self, attrs=None):
        super().__init__(attrs, format='%Y-%m-%dT%H:%M')


class BookingForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('start_time', 'finish_time',)
        widgets = {
            'start_time': DateTimeInput,
            'finish_time': DateTimeInput,
        }

    def clean_finish_time(self):
        start_time = self.cleaned_data['start_time']
        finish_time = self.cleaned_data['finish_time']
        if finish_time <= start_time:
            self.add_error(NON_FIELD_ERRORS, 'Время окончания не может быть меньше,'
                                             ' или равным времени начала бронирования!')
        return finish_time

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < timezone.now():
            self.add_error(NON_FIELD_ERRORS, 'Время начала бронирования не может быть меньше текущей даты!')
        return start_time
