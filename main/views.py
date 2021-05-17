import requests
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from main.models import KazTour


def index(request):
    return render(request, "main/index.html")


def about(request):
    return render(request, "main/about.html")


def tours(request):
    all_tours = KazTour.objects.all()
    return render(request, "main/tours.html", {'all_tours': all_tours})


def profile(request):
    return render(request, "main/profile.html")


def akmola(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Kokshetau'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/akmola.html", {'city_weather': city_weather})


def aktobe(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Aktobe'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/aktobe.html", {'city_weather': city_weather})
