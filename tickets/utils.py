from tickets.models import Flights


def from_search(query):
    return Flights.objects.filter(departure_airport__city=str(query))

def to_search(query):
    return Flights.objects.filter(arrival_airport__city=str(query))

def departure_date_search(query):
    return Flights.objects.filter(departure_time__date=query)

def arrival_date_search(query):
    return Flights.objects.filter(arrival_time__date=query)