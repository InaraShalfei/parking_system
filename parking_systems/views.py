from django.shortcuts import render, redirect, get_object_or_404

from parking_systems.forms import BookingForm
from parking_systems.models import Parking, Reservation


def index(request):
    parking_slots = Parking.objects.all()
    return render(request, 'parking_systems/index.html', {'parking_slots': parking_slots})


def booking(request):
    form = BookingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        reservation = form.save(commit=False)
        reservation.parking_space = Parking.objects.first()
        reservation.save()
        return redirect('parking_systems:reservation', reservation_id=reservation.id)
    return render(request, 'parking_systems/booking.html', {'form': form})


def reservation(request, reservation_id):
    #TODO: formatting of period representation in template
    reservation = get_object_or_404(Reservation, id=reservation_id)
    period = reservation.finish_time - reservation.start_time
    return render(request, 'parking_systems/reservation.html', {'reservation': reservation, 'period': period})


def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    form = BookingForm(request.POST or None, instance=reservation)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('parking_systems:reservation', reservation_id=reservation.id)
    return render(request, 'parking_systems/booking.html', {'form': form, 'reservation': reservation})


def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('parking_systems:index')
    return render(request, 'includes/delete_reservation.html', {'reservation': reservation})
