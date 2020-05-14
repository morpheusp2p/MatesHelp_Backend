from django.db import models

from locations.models import Type

from tinymce.models import HTMLField

# Create your models here.
class Page(models.Model):
    name = models.CharField(max_length=250)
    banner_image = models.ImageField(upload_to = 'images/')
    description = HTMLField()
    categories = models.ManyToManyField(Type)

    def __str__(self):
        return self.name
