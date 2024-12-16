from django.core.paginator import Paginator
from django.shortcuts import render
from tickets.models import Airports, Bookings, Flights, Seats, Ticket_flights, Tickets
from tickets.utils import arrival_date_search, departure_date_search, from_search, to_search


def flight(request):
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', None)
    from_location = request.GET.get('from', None)
    to_location = request.GET.get('to', None)
    departure_date = request.GET.get('departure_date', None)
    return_date = request.GET.get('return_date', None)
    passengers = int(request.GET.get("passengers", 1))
    fare_conditions = request.GET.get("tariff", None)
    
    flights = Flights.objects.all()
    bookings = Bookings.objects.all()
    
    if from_location:
        flights = from_search(from_location)
    if to_location:
        flights = to_search(to_location)
    if departure_date:
        flights = departure_date_search(departure_date)
    if return_date:
        flights = arrival_date_search(return_date)
    
    # Применение фильтрации по классу обслуживания
    if fare_conditions:
        flights = flights.filter(ticket_flights__fare_conditions=fare_conditions)
    
    if order_by and order_by != "default":
        bookings = bookings.order_by(order_by)
        
    
    paginator = Paginator(flights, 3)
    current_page = paginator.page(int(page))
    
    context= {
        "title": "Avia - Билеты",
        "flights": current_page,
        "bookings": bookings,
        "passengers": passengers,
        "fare_conditions": fare_conditions,
    }
    return render(request, 'tickets/flight.html', context)
    
def booking(request):
    return render(request, 'tickets/booking.html')