import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView

from main.forms import CheckoutForm
from main.models import *


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


class CheckUser(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = TourCart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user:
                cart_obj.customer = request.user
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


class AddToCartView(CheckUser, TemplateView):
    template_name = "main/addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = KazTour.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = TourCart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.tourcartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
            # new item is added in cart
            else:
                cartproduct = TourCartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
                cart_obj.total += product_obj.price
                cart_obj.save()

        else:
            cart_obj = TourCart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = TourCartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1, subtotal=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()

        return context


class MyCartView(CheckUser, TemplateView):
    template_name = "main/mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = TourCart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


class ManageCartView(CheckUser, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = TourCartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("mycart")


class EmptyCartView(CheckUser, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = TourCart.objects.get(id=cart_id)
            cart.tourcartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("mycart")


class CheckoutView(CheckUser, CreateView):
    template_name = "main/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("tours")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = TourCart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = TourCart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.total = cart_obj.total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
            order = form.save()
        else:
            return redirect("tours")
        return super().form_valid(form)


class CustomerProfileView(CheckUser, TemplateView):
    template_name = "main/customerprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user:
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context


class CustomerOrderDetailView(CheckUser, DetailView):
    template_name = "main/customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user != order.cart.customer:
                return redirect("customerprofile")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)


def planyourtrip(request):
    return render(request, "main/planyourtrip.html")


def akmola(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
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
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
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


def kostanay(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Kostanay'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/kostanay.html", {'city_weather': city_weather})


def kyzylorda(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Kyzylorda'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/kyzylorda.html", {'city_weather': city_weather})


def atyrau(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Atyrau'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/Atyrau.html", {'city_weather': city_weather})


def westkz(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Oral'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/westkz.html", {'city_weather': city_weather})


def karagandy(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Karagandy'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/karagandy.html", {'city_weather': city_weather})


def northkz(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Petropavl'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/northkz.html", {'city_weather': city_weather})


def pavlodar(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Pavlodar'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/pavlodar.html", {'city_weather': city_weather})


def eastkz(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Oskemen'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/eastkz.html", {'city_weather': city_weather})


def almaty(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Almaty'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/almaty.html", {'city_weather': city_weather})


def mangystau(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Aktau'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/mangystau.html", {'city_weather': city_weather})


def southkz(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Shymkent'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/southkz.html", {'city_weather': city_weather})


def zhambyl(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=78188f6bb68d92e1918239bccf8980ac'
    city = 'Taraz'

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon']
    }
    print(city_weather)
    return render(request, "main/zhambyl.html", {'city_weather': city_weather})
