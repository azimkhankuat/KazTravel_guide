from django.shortcuts import render
from django.http import HttpResponse
from .models import Tour


# Create your views here.
def index(request):
    return render(request, "main/index.html")


def about(request):
    return render(request, "main/about.html")


def tours(request):
    all_tours = Tour.objects.all()
    return render(request, "main/tours.html", {'all_tours': all_tours})
