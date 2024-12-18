from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import F, DecimalField, ExpressionWrapper, IntegerField, Min, OuterRef, Subquery
from django.shortcuts import render
from tickets.models import Flights
from tickets.utils import arrival_date_search, departure_date_search, from_search, tariff_search, to_search

def flight(request):
    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', None)
    from_location = request.GET.get('from', None)
    to_location = request.GET.get('to', None)
    departure_date = request.GET.get('departure_date', None)
    return_date = request.GET.get('return_date', None)
    passengers = int(request.GET.get('passengers', 1))
    tariff_name = request.GET.get('tariff', None)

    flights = Flights.objects.all()

    # Применение фильтров
    if from_location:
        flights = flights.filter(departure_airport__city__icontains=from_location)
    if to_location:
        flights = flights.filter(arrival_airport__city__icontains=to_location)
    if departure_date:
        flights = flights.filter(departure_time__date=departure_date)
    
    # Применение фильтра по тарифу
    # Применение фильтра по тарифу
    if tariff_name:
        if tariff_name == 'Комфорт':
            # Используем ExpressionWrapper для создания вычисляемого поля
            flights = flights.annotate(
                adjusted_price=ExpressionWrapper(F('price') * 1.5, output_field=DecimalField())
            )
        elif tariff_name == 'Бизнес':
            flights = flights.annotate(
                adjusted_price=ExpressionWrapper(F('price') * 2, output_field=DecimalField())
            )
        else:  # Эконом
            flights = flights.annotate(
                adjusted_price=ExpressionWrapper(F('price'), output_field=DecimalField())
            )
    else:
        # Если тариф не выбран, возвращаем исходные значения
        flights = flights.annotate(
            adjusted_price=ExpressionWrapper(F('price'), output_field=DecimalField())
        )

    # Умножение на количество пассажиров
    flights = flights.annotate(final_price=F('adjusted_price') * passengers)
    
    # Если дата обратного рейса выбрана, суммируем цену туда и обратно
    if return_date:
        flights = flights.annotate(final_price=F('final_price') + F('adjusted_price') * passengers)

    # Сортировка
    if order_by and order_by != "default":
        if order_by == "price":
            flights = flights.order_by("price")
        elif order_by == "-price":
            flights = flights.order_by("-price")
            
    paginator = Paginator(flights, 3)
    current_page = paginator.page(int(page))

    context = {
        "title": "Avia - Билеты",
        "passengers": passengers,
        "flights": current_page,
        "tariff_name": tariff_name,
    }
    return render(request, 'tickets/flight.html', context)

def booking(request):
    return render(request, 'tickets/booking.html')
