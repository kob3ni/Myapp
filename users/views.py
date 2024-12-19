import csv
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from tickets.models import Booking
from openpyxl import Workbook

from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")
                
                if request.POST.get('next', None):
                     return HttpResponseRedirect(request.POST.get('next'))

                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
                
    context = {
        'title': 'Avia - Авторизация',
        'form': form        
    }
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f"{user.username}, Вы успешно зарегистрировались и вошли в аккаунт")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
        
    context = {
        'title': 'Avia - Регистрация',
        'form': form 
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)
        
    # Проверка на принадлежность к группе "Сотрудники"
    if request.user.groups.filter(name="Сотрудники").exists() or request.user.is_superuser:
        # Если сотрудник или суперпользователь — показываем все бронирования
        bookings = Booking.objects.all()
    else:
        # Иначе показываем только бронирования текущего пользователя
        bookings = Booking.objects.filter(user=request.user)
    
    context = {
        'title': 'Avia - Профиль',
        'form': form,
        'bookings': bookings  # Передаем бронирования в контекст
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))

def export_bookings_json(request):
    """Экспорт бронирований в формате JSON."""
    bookings = Booking.objects.all().values(
        'id', 'flight__id', 'passengers', 'tariff__name', 'total_price', 'created_at', 'user__username'
    )
    data = list(bookings)
    return JsonResponse(data, safe=False)

def export_bookings_xlsx(request):
    """Экспорт бронирований в формате XLSX."""
    bookings = Booking.objects.all().values(
        'id', 'flight__id', 'passengers', 'tariff__name', 'total_price', 'created_at', 'user__username'
    )
    
    # Создание книги Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Bookings"
    
    # Заголовки столбцов
    ws.append(['ID', 'Flight', 'Passengers', 'Tariff', 'Total Price', 'Created At', 'User'])

    # Заполнение данными
    for booking in bookings:
        created_at = booking.get('created_at')  
        # Если есть информация о временной зоне, удаляем её
        if created_at:
            # Если есть информация о временной зоне, удаляем её
            if created_at.tzinfo is not None:
                created_at = created_at.replace(tzinfo=None)
            
            # Добавляем строку в Excel с форматом даты и времени
            created_at_str = created_at.strftime('%d.%m.%Y %H:%M')
        else:
            created_at_str = "N/A"  # Если дата отсутствует, отображаем "N/A"
            
        ws.append([
            booking['id'],
            booking['flight__id'],
            booking['passengers'],
            booking['tariff__name'],
            booking['total_price'],
            created_at_str,
            booking['user__username']
        ])

    # Настроить HTTP-ответ для загрузки Excel файла
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="bookings.xlsx"'

    # Сохраняем книгу в HTTP-ответ
    wb.save(response)

    return response