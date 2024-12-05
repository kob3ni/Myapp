from django.shortcuts import render

def flight(request):
    context= {
        "title": "Home - Билеты",
        "tickets":[
            {
                "direction_to": "Москва →  Санкт-Петербург",
                "direction_from": "Санкт-Петербург → Москва",
                "price": 2100,
            },
            {
                "direction_to": "Москва → Казань",
                "direction_from": "Казань → Москва",
                "price": 3200,
            },
            {
                "direction_to": "Москва → Калининград",
                "direction_from": "Калининград → Москва",
                "price": 4500,
            },
            {
                "direction_to": "Москва → Самара",
                "direction_from": "Самара → Москва",
                "price": 5800,
            },
                        {
                "direction_to": "Москва → Екатеринбург",
                "direction_from": "Екатеринбург → Москва",
                "price": 5800,
            },
            {
                "direction_to": "Москва → Тюмень",
                "direction_from": "Тюмень → Москва",
                "price": 5800,
            },
            {
                "direction_to": "Москва → Красноярск",
                "direction_from": "Красноярск → Москва",
                "price": 5800,
            },                        
            {
                "direction_to": "Москва → Омск",
                "direction_from": "Омск → Москва",
                "price": 5800,
            }, 
            {
                "direction_to": "Москва → Мурманск",
                "direction_from": "Мурманск → Москва",
                "price": 5800,
            }, 
            {
                "direction_to": "Москва → Уфа",
                "direction_from": "Уфа → Москва",
                "price": 5800,
            }, 
        ]
    }
    return render(request, 'tickets/flight.html', context)
    
def booking(request):
    return render(request, 'tickets/booking.html')