from django.urls import path

from tickets import views

app_name = 'tickets'

urlpatterns = [
    path('', views.flight, name='index'),
    path('search/', views.flight, name='search'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
]