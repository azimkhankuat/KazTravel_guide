from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class KazTour(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.TextField()
    price = models.PositiveIntegerField()
    duration = models.TextField('Duration of the tour')
    price_include = models.TextField('Prices include')
    description = models.TextField()
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class TourCart(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class TourCartProduct(models.Model):
    cart = models.ForeignKey(TourCart, on_delete=models.CASCADE)
    product = models.ForeignKey(KazTour, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)