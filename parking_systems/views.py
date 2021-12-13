from django.contrib.auth.decorators import permission_required
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

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
        start_time = form.cleaned_data['start_time']
        finish_time = form.cleaned_data['finish_time']
        occupied_parkings = Reservation.objects.filter(Q(
            start_time__lte=start_time,
            finish_time__gte=start_time
        ) | Q(
            start_time__lte=finish_time,
            finish_time__gte=finish_time
        ) | Q(
            start_time__gte=start_time,
            finish_time__lte=finish_time
        )).values('parking_space_id')
        free_parking = Parking.objects.exclude(id__in=occupied_parkings).first()
        if free_parking:
            reservation.parking_space = free_parking
            reservation.save()
            return redirect('parking_systems:reservation', reservation_id=reservation.id)
        else:
            form.add_error(NON_FIELD_ERRORS, 'Нет свободных парковочных мест!')
    return render(request, 'parking_systems/booking.html', {'form': form})


@permission_required('parking_systems.view_reservation')
def reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    period = reservation.finish_time - reservation.start_time
    return render(request, 'parking_systems/reservation.html', {'reservation': reservation, 'period': period,
                                                                'slot': reservation.parking_space})


@permission_required('parking_systems.change_reservation')
def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    parking_slot_reservations = reservation.parking_space.reservations
    form = BookingForm(request.POST or None, instance=reservation)
    if request.method == 'POST' and form.is_valid():
        start_time = form.cleaned_data['start_time']
        finish_time = form.cleaned_data['finish_time']
        occupied_time = parking_slot_reservations.filter(Q(
            start_time__lte=start_time,
            finish_time__gte=start_time
        ) | Q(
            start_time__lte=finish_time,
            finish_time__gte=finish_time
        ) | Q(
            start_time__gte=start_time,
            finish_time__lte=finish_time
        )).exclude(id=reservation.id).exists()
        if not occupied_time:
            form.save()
            return redirect('parking_systems:reservation', reservation_id=reservation.id)
        else:
            form.add_error(NON_FIELD_ERRORS, 'Выбранное время занято для данного парковочного места!')
    return render(request, 'parking_systems/booking.html', {'form': form, 'reservation': reservation})


@permission_required('parking_systems.delete_reservation')
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('parking_systems:parking_reservations', parking_slot=reservation.parking_space.id)
