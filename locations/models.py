from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField


class Type(models.Model):
    # Type Model
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    # Location Model
    name = models.CharField(max_length=250)
    location = models.PointField()
    website = models.URLField(null=True, blank=True,)
    address = models.CharField(null=True, blank=True, max_length=550)
    suburb = models.CharField(null=True, blank=True, max_length = 250)
    type = models.ForeignKey(Type, null=True, blank=True, on_delete=models.CASCADE)
    desc = models.TextField(null=True, blank=True)
    opening_days = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
