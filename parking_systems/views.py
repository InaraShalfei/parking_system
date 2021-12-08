from django.shortcuts import render, redirect

from parking_systems.forms import BookingForm
from parking_systems.models import Parking


def index(request):
    parking_slots = Parking.objects.all()
    return render(request, 'parking_systems/index.html', {'parking_slots': parking_slots})


def booking(request):
    form = BookingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        reservation = form.save(commit=False)
        reservation.parking_space = Parking.objects.first()
        reservation.save()
        return redirect('parking_systems:index')
    return render(request, 'parking_systems/booking.html', {'form': form})


