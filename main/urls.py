from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('tours', AllToursView.as_view(), name="tours"),
    path('tour_details/<slug:slug>/', TourDetailView.as_view(), name="tourdetails"),
    path('profile', views.profile, name="profile"),
    path('akmola', views.akmola, name="akmola"),
    path('aktobe', views.aktobe, name="aktobe")
]