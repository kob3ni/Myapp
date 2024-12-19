from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, DecimalField, ExpressionWrapper
from django.shortcuts import get_object_or_404, redirect, render
from tickets.models import Flights, Booking, Tariff

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

    # Сохранение final_price, пассажиров и тарифа в сессии для дальнейшего использования
    if flights.exists():
        final_price = flights.first().final_price
        request.session['final_price'] = str(final_price)
        request.session['passengers'] = passengers
        request.session['tariff_name'] = tariff_name
        
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

@login_required
def book_flight(request, flight_id):
    # Получение данных о рейсе
    flight = get_object_or_404(Flights, id=flight_id)

    passengers = int(request.session.get('passengers', 1))  # Получаем количество пассажиров
    tariff_name = request.session.get('tariff_name', 'Эконом')  # Получаем тариф
    final_price = Decimal(request.session.get('final_price', 0))  # Получаем final_price

    # Получение тарифа
    tariff = get_object_or_404(Tariff, name=tariff_name)
    
    # Создание записи бронирования
    booking = Booking.objects.create(
        flight=flight,
        passengers=passengers,
        tariff=tariff,
        total_price=final_price,
        user=request.user
    )
    booking.save()

    # Сообщение пользователю
    messages.success(request, 'Ваше бронирование успешно создано!')

    # Перенаправление на страницу с бронированиями
    return redirect('users:profile') 

def delete_booking(request, booking_id):
    # Получаем бронирование по ID
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Проверяем, что пользователь является администратором или стаффом
    if request.user.is_staff or request.user.is_superuser:
        booking.delete()  # Удаляем бронирование
    
    return redirect('users:profile')
