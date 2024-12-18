from django.contrib import admin

from tickets.models import Airports, Flights, Tariff, Aircrafts, Booking
# Register your models here.
admin.site.register(Airports)
admin.site.register(Booking)
admin.site.register(Flights)
admin.site.register(Tariff)
admin.site.register(Aircrafts)
