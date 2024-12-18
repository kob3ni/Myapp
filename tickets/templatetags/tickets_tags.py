from django import template
from django.utils.http import urlencode
from tickets.models import Flights, Airports

register = template.Library()

@register.simple_tag()
def tag_flights():
    return Flights.objects.all()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)

@register.filter
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return value
