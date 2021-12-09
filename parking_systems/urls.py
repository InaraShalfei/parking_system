from django.urls import path

from . import views

app_name = 'parking_systems'

urlpatterns = [
    path('', views.index, name='index'),
    path('booking/', views.booking, name='booking'),
    path('booking/<int:reservation_id>/', views.reservation, name='reservation'),
    path('booking/<int:reservation_id>/update', views.update_reservation, name='update_reservation'),
    path('booking/<int:reservation_id>/delete', views.delete_reservation, name='delete_reservation'),

    ]