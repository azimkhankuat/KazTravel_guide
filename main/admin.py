from django.contrib import admin
from .models import *

admin.site.register(
    [Category, KazTour, TourCart, TourCartProduct, Order])
