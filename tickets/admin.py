from django.contrib import admin

from tickets.models import Aircrafts, Airports, Bookings, Tickets, Flights, Ticket_flights, Seats
# Register your models here.

admin.site.register(Aircrafts)
admin.site.register(Airports)
admin.site.register(Bookings)
admin.site.register(Tickets)
admin.site.register(Flights)
admin.site.register(Ticket_flights)
admin.site.register(Seats)
