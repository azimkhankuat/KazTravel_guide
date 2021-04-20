from django.db import models


class Tour(models.Model):
    title = models.TextField('Title of the tour')
    desc = models.TextField('Description of the tour')

    def __str__(self):
        return self.title
