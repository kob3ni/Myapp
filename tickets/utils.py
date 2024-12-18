from tickets.models import Flights


def from_search(query):
    return Flights.objects.filter(departure_airport__city__contains=str(query))

def to_search(query):
    return Flights.objects.filter(arrival_airport__city__contains=str(query))

def departure_date_search(query):
    return Flights.objects.filter(departure_time__date=query)

def arrival_date_search(query):
    return Flights.objects.filter(arrival_time__date=query)

def tariff_search(query):
    return Flights.objects.filter(tickets__tariff__name=query)