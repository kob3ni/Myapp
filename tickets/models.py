from decimal import Decimal
from django.db import models
from datetime import timedelta

class Aircrafts(models.Model):
    model = models.TextField(verbose_name='Модель самолета')
    
    class Meta:
        db_table = 'aircraft'
        verbose_name = 'Самолет'
        verbose_name_plural = 'Самолеты'
    
    def __str__(self):
        return self.model
        
class Airports(models.Model):
    airport_name = models.TextField(verbose_name='Название аэропорта')
    city = models.TextField(verbose_name='Город')
    timezone = models.TextField(verbose_name='Часовой пояс')
    iata_code = models.CharField(max_length=3, verbose_name='IATA код')
    
    class Meta:
        db_table = 'airport'
        verbose_name = 'Аэропорт'
        verbose_name_plural = 'Аэропорты'
    
    def __str__(self):
        return f"{self.airport_name} ({self.iata_code})" 
        
class Bookings(models.Model):
    book_date_start = models.DateTimeField(verbose_name='Дата начала брони')
    book_date_end = models.DateTimeField(verbose_name='Дата окончания брони')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Полная сумма')
    
    class Meta:
        db_table = 'booking'
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        
    def __str__(self):
        return f"Бронирование: {self.book_date_start} - {self.book_date_end}"
                        
class Tickets(models.Model):
    passenger_id = models.CharField(max_length=20, verbose_name='Идентификатор пассажира')
    passenger_name = models.TextField(verbose_name='ФИО пассажира')
    book_ref = models.ForeignKey(to=Bookings, on_delete=models.CASCADE, verbose_name='Номер бронирования')

    class Meta:
        db_table = 'ticket'
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
    
    def __str__(self):
        return self.passenger_name
    
class Flights(models.Model):
    departure_time = models.DateTimeField(verbose_name='Время вылета')
    arrival_time = models.DateTimeField(verbose_name='Время прибытия')
    departure_airport = models.ForeignKey(to=Airports, on_delete=models.CASCADE, 
                                          related_name = 'departure_airports',
                                          verbose_name='Аэропорт вылета')
    arrival_airport = models.ForeignKey(to=Airports, on_delete=models.CASCADE, 
                                        related_name = 'arrival_airports',
                                        verbose_name='Аэропорт прибытия')
    aircraft_code = models.ForeignKey(to=Airports, on_delete=models.CASCADE, 
                                      related_name = 'aircraft_codes', 
                                      verbose_name='Код самолета')
    
    
    class Meta:
        db_table = 'flight'
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ("id",)
        
    def __str__(self):
        return f'{self.departure_airport} → {self.arrival_airport} ({self.departure_time:%Y-%m-%d %H:%M})'
    
    def get_flight_duration(self):
        """
        Вычисляет длительность полета.

        :param flight: Экземпляр модели Flights
        :return: Строка в формате "X ч Y мин"
        """
        if self.departure_time and self.arrival_time:
            # Вычисляем разницу между временем прибытия и временем вылета
            duration = self.arrival_time - self.departure_time

            # Преобразуем длительность в часы и минуты
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes = remainder // 60

            return f"{int(hours)} ч {int(minutes)} мин"
        else:
            return "Нет данных"

                
class Ticket_flights(models.Model):
    fare_conditions = models.CharField(max_length=10, verbose_name='Класс обслуживания')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    flight_id = models.ForeignKey(to=Flights, on_delete=models.CASCADE, verbose_name='Идентификатор рейса')
    ticket_no = models.ForeignKey(to=Tickets, on_delete=models.CASCADE, verbose_name='Номер билета')
    
    class Meta:
        db_table = 'ticket flight'
        verbose_name = 'Перелет'
        verbose_name_plural = 'Перелеты'
    
class Seats(models.Model):
    fare_conditions = models.CharField(max_length=10, verbose_name='Класс обслуживания')
    aircraft_code = models.ForeignKey(to=Airports, on_delete=models.CASCADE, verbose_name='Код самолета')
    
    class Meta:
        db_table = 'seat'
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
    
    def __str__(self):
        return self.fare_conditions