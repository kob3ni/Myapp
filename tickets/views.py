from django.core.paginator import Paginator
from django.shortcuts import render
from tickets.models import Airports, Bookings, Flights, Seats, Ticket_flights, Tickets


def flight(request):
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', None)
    
    flights = Flights.objects.all()
    bookings = Bookings.objects.all()
    
    if order_by and order_by != "default":
        bookings = bookings.order_by(order_by)
    
    paginator = Paginator(flights, 3)
    current_page = paginator.page(int(page))
    
    context= {
        "title": "Avia - Билеты",
        "flights": current_page,
        "bookings": bookings,
    }
    return render(request, 'tickets/flight.html', context)
    
def booking(request):
    return render(request, 'tickets/booking.html')