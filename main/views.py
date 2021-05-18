import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

from main.models import KazTour, Category


def index(request):
    return render(request, "main/index.html")


def about(request):
    return render(request, "main/about.html")


class AllToursView(TemplateView):
    template_name = "main/tours.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


class TourDetailView(TemplateView):
    template_name = "main/tour_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = KazTour.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context


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
