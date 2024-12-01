from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {
        'title' : 'Home', 
        'conyent' : 'Главная страница'
    }
    return render(request, 'main/index.html', context)
