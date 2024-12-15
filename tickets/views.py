from django.core.paginator import Paginator
from django.shortcuts import render
from tickets.models import Airports, Bookings, Flights, Seats, Ticket_flights, Tickets


def flight(request):
    page = request.GET.get('page', 1)
    
    flights = Flights.objects.all()
    
    paginator = Paginator(flights, 1)
    current_page = paginator.page(int(page))
    
    context= {
        "title": "Avia - Билеты",
        "flights": current_page,
    }
    return render(request, 'tickets/flight.html', context)
    
def booking(request):
    return render(request, 'tickets/booking.html')