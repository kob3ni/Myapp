from django.urls import path

from tickets import views

app_name = 'tickets'

urlpatterns = [
    path('', views.flight, name='index'),
    path('search/', views.flight, name='search'),
    path('booking/', views.booking, name='booking'),
]