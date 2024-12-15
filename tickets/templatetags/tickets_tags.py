from django import template
from tickets.models import Flights, Airports

register = template.Library()

@register.simple_tag()
def tag_flights():
    return Flights.objects.all()
