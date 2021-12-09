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

    def clean_finish_time(self):
        start_time = self.cleaned_data['start_time']
        finish_time = self.cleaned_data['finish_time']
        if finish_time <= start_time:
            raise forms.ValidationError('Время окончания не может быть меньше, или равным времени начала бронирования!')
        return finish_time, start_time
