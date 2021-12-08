from django.urls import path

from . import views

app_name = 'parking_systems'

urlpatterns = [
    path('', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
    path('booking/<int:reservation_id>/', views.reservation, name='reservation'),

    ]