from django.shortcuts import render


def index(request):
    return render(request, 'parking_systems/index.html')
