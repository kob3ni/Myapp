from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('export/bookings/json/', views.export_bookings_json, name='export_bookings_json'),
    path('export/bookings/xlsx/', views.export_bookings_xlsx, name='export_bookings_xlsx'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]