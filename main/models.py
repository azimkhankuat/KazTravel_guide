from django.db import models


class Tour(models.Model):
    title = models.TextField('Title of the tour')
    type = models.TextField('Type of the tour')
    desc = models.TextField('Description of the tour')
    price = models.IntegerField('Price of the tour')
    duration = models.TextField('Duration of the tour')
    price_include = models.TextField('Prices include')
    image = models.TextField('Image link')

    def __str__(self):
        return self.title
