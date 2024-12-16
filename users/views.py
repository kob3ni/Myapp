from django.shortcuts import render

def login(request):
    context = {
        'title': 'Avia - Авторизация'
    }
    return render(request, 'users/login.html', context)

def registration(request):
    context = {
        'title': 'Avia - Регистрация'
    }
    return render(request, 'users/registration.html', context)

def profile(request):
    context = {
        'title': 'Avia - Профиль'
    }
    return render(request, 'users/profile.html', context)

def logout(request):
    ...