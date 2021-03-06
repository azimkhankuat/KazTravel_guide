from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('tours', AllToursView.as_view(), name="tours"),
    path('tour_details/<slug:slug>/', TourDetailView.as_view(), name="tourdetails"),
    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(), name="customerorderdetail"),
    path("planyourtrip/", views.planyourtrip, name="planyourtrip"),
    path('akmola', views.akmola, name="akmola"),
    path('aktobe', views.aktobe, name="aktobe"),
    path('kostanay', views.kostanay, name="kostanay"),
    path('kyzylorda', views.kyzylorda, name="kyzylorda"),
    path('atyrau', views.atyrau, name="atyrau"),
    path('westkz', views.westkz, name="westkz"),
    path('karagandy', views.karagandy, name="karagandy"),
    path('northkz', views.northkz, name="northkz"),
    path('pavlodar', views.pavlodar, name="pavlodar"),
    path('eastkz', views.eastkz, name="eastkz"),
    path('almaty', views.almaty, name="almaty"),
    path('mangystau', views.mangystau, name="mangystau"),
    path('southkz', views.southkz, name="southkz"),
    path('zhambyl', views.zhambyl, name="zhambyl")
]