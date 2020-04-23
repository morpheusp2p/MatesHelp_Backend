from django.contrib.gis.db import models

class Type(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=250)
    location = models.PointField()
    website = models.URLField(null=True, blank=True,)
    address = models.CharField(null=True, blank=True, max_length=550)
    suburb = models.CharField(null=True, blank=True, max_length = 250)
    type = models.ForeignKey(Type, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
