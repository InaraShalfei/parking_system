from django import forms

from parking_systems.models import Reservation


class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'


class BookingForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('start_time', 'finish_time',)
        widgets = {
            'start_time': DateTimeInput,
            'finish_time': DateTimeInput,
        }
