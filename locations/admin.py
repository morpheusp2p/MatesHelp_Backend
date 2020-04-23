from django.contrib import admin

from .models import Location, Type

admin.site.register(Type)
admin.site.register(Location)
