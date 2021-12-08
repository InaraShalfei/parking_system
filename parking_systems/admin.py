from django.contrib import admin

from parking_systems.models import Parking, Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_filter = ('start_time', )
    empty_value_display = '-пусто-'


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Parking)
