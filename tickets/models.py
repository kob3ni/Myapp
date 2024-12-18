from decimal import Decimal
from django.db import models
        
class Airports(models.Model):
    airport_name = models.TextField(verbose_name='Название аэропорта')
    city = models.TextField(verbose_name='Город')
    iata_code = models.CharField(max_length=3, unique=True, verbose_name='IATA код')
    
    class Meta:
        db_table = 'airport'
        verbose_name = 'Аэропорт'
        verbose_name_plural = 'Аэропорты'
    
    def __str__(self):
        return f"{self.airport_name} ({self.iata_code})" 
    
class Aircrafts(models.Model):
    model = models.CharField(max_length=30, verbose_name='Модель самолета')
    
    class Meta:
        db_table = 'aircraft'
        verbose_name = 'Самолет'
        verbose_name_plural = 'Самолеты'
        
    def __str__(self):
        return self.model
    
    
class Flights(models.Model):
    departure_time = models.DateTimeField(verbose_name='Время вылета')
    arrival_time = models.DateTimeField(verbose_name='Время прибытия')
    departure_airport = models.ForeignKey(to=Airports, on_delete=models.CASCADE, 
                                          related_name = 'departure_airports',
                                          verbose_name='Аэропорт вылета')
    arrival_airport = models.ForeignKey(to=Airports, on_delete=models.CASCADE, 
                                        related_name = 'arrival_airports',
                                        verbose_name='Аэропорт прибытия')
    aircraft_code = models.ForeignKey(to=Aircrafts, on_delete=models.CASCADE, 
                                      related_name = 'aircraft_codes', 
                                      verbose_name='Код самолета')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    
    class Meta:
        db_table = 'flight'
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ("id",)
        
    def __str__(self):
        return f'{self.departure_airport.city} → {self.arrival_airport.city} ({self.departure_time:%Y-%m-%d %H:%M})'
    
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

class Tariff(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название тарифа')  # Название тарифа
    
    class Meta:
        db_table = 'tariff'
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.name
                
class Booking(models.Model):
    """
    Таблица для хранения информации о билетах.
    """
    flight = models.ForeignKey(Flights, related_name='bookings', on_delete=models.CASCADE)
    passengers = models.PositiveIntegerField()  # Количество пассажиров
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)  # Тариф
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Итоговая цена за бронирование
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'booking'
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f"Ticket for {self.flight} ({self.tariff}) - {self.price} ₽"
    