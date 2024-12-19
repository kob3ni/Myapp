from django import forms

from tickets.models import Flights


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flights
        fields = [
            'departure_airport', 
            'arrival_airport', 
            'departure_time', 
            'arrival_time', 
            'price',
            'aircraft_code'] 