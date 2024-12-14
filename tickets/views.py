from django.shortcuts import render
from tickets.models import Airports, Bookings, Flights, Seats, Ticket_flights, Tickets


def flight(request):
    
    flights = Flights.objects.all()
    airports = Airports.objects.all()
    
    context= {
        "title": "Avia - Билеты",
        "flights": flights,
        "airports": airports,
    }
    return render(request, 'tickets/flight.html', context)
    
def booking(request):
    return render(request, 'tickets/booking.html')