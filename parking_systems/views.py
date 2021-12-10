from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from parking_systems.forms import BookingForm
from parking_systems.models import Parking, Reservation


@permission_required('parking_systems.view_parking')
def index(request):
    parking_slots = Parking.objects.all()
    return render(request, 'parking_systems/index.html', {'parking_slots': parking_slots})


@permission_required('parking_systems.add_parking')
def add_parking(request):
    Parking.objects.create()
    return redirect('parking_systems:index')


@permission_required('parking_systems.delete_parking')
def delete_parking(request, parking_slot):
    parking_slot = get_object_or_404(Parking, id=parking_slot)
    if request.method == 'POST':
        parking_slot.delete()
        return redirect('parking_systems:index')
    return render(request, 'includes/delete_parking.html', {'slot': parking_slot})


@permission_required('parking_systems.view_reservation')
def parking_reservations(request, parking_slot):
    parking_slot = get_object_or_404(Parking, id=parking_slot)
    reservations = parking_slot.reservations.all()
    paginator = Paginator(reservations, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'parking_systems/reservations.html', {'slot': parking_slot, 'page': page})


@permission_required('parking_systems.add_reservation')
def booking(request):
    form = BookingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        reservation = form.save(commit=False)
        reservation.parking_space = Parking.objects.first()
        reservation.save()
        return redirect('parking_systems:reservation', reservation_id=reservation.id)
    return render(request, 'parking_systems/booking.html', {'form': form})


@permission_required('parking_systems.view_reservation')
def reservation(request, reservation_id):
    #TODO: formatting of period representation in template
    reservation = get_object_or_404(Reservation, id=reservation_id)
    period = reservation.finish_time - reservation.start_time
    return render(request, 'parking_systems/reservation.html', {'reservation': reservation, 'period': period,
                                                                'slot': reservation.parking_space})


@permission_required('parking_systems.change_reservation')
def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    form = BookingForm(request.POST or None, instance=reservation)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('parking_systems:reservation', reservation_id=reservation.id)
    return render(request, 'parking_systems/booking.html', {'form': form, 'reservation': reservation})


@permission_required('parking_systems.delete_reservation')
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('parking_systems:parking_reservations', parking_slot=reservation.parking_space.id)
    return render(request, 'includes/delete_reservation.html', {'reservation': reservation})
