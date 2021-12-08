from django.shortcuts import render

from parking_systems.models import Parking


def index(request):
    parking_slots = Parking.objects.all()
    return render(request, 'parking_systems/index.html', {'parking_slots': parking_slots})
