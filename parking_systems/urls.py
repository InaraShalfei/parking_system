from django.urls import path

from . import views

app_name = 'parking_systems'

urlpatterns = [
    path('', views.index, name='index'),
    ]